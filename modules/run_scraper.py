import logging
import os
from datetime import datetime
from bs4 import BeautifulSoup
import json
import time

from dotenv import load_dotenv
from modules.db_vacantes import init_db, insert_vacante
from lib.linkedin_jobs_scraper import LinkedinScraper
from lib.linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from lib.linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from lib.linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, OnSiteOrRemoteFilters

load_dotenv()

# Silenciar logs innecesarios
logging.basicConfig(level=logging.ERROR)
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('li:scraper').setLevel(logging.ERROR)

def clean_text(text):
    if not text:
        return ""
    soup = BeautifulSoup(text, "html.parser")
    return ' '.join(soup.get_text().split())

def run_scraper():
    start_time = time.time()
    print(f"🚀 Ejecutando run_scraper() a {start_time}")
    
    
    init_db()

    LI_AT = os.getenv("LI_AT_COOKIE")
    if not LI_AT:
        raise Exception("❌ Cookie LI_AT_COOKIE no encontrada en .env")

    results = []

    def on_data(data: EventData):
        print(f"[DATA] {data.title} @ {data.company} | {data.place}")
        print(f"       Link: {data.link}\n")

        insert_vacante({
            "qry_title": data.query,
            "qry_loc": data.location,
            "title": data.title,
            "company": data.company,
            "location": data.place,
            "date": data.date.strftime('%Y-%m-%d') if hasattr(data.date, 'strftime') else str(data.date),
            "date_text": data.date_text,
            "insights": json.dumps(data.insights or []),  # JSON para mantener formato
            "link": data.link,
            "job_description": data.description or "",
            "full_text": clean_text(data.description),
            "scraped_at": datetime.today().strftime('%Y-%m-%d'),
            "modalidad_trabajo": extract_modality(data.insights),
        })

        results.append(data.link)

    def on_error(error):
        print('[ERROR]', error)

    def on_end():
        print('[END] Fin de un query.')

    scraper = LinkedinScraper(
        headless=True,
        max_workers=1,
        slow_mo=0.6,
        page_load_timeout=40,
    )

    scraper.on(Events.DATA, on_data)
    scraper.on(Events.ERROR, on_error)
    scraper.on(Events.END, on_end)

    # Búsquedas
# Definiciones modulares para combinaciones
    roles = [
        "VP", "Vice President", "Director", "Head", "Executive"
    ]

    functions = [
        "Procurement", "Sourcing", "Purchasing", "Commodity", "Category"
    ]

    # Combinaciones automáticas tipo tabla 2x2
    query_keywords = [f"{role} {func}" for role in roles for func in functions]

    locations = [
        "Nuevo León, México", "Mexico", "Remote",
        "United States", "Canada", "Remote United States", "Remote Canada"
    ]

    queries = [
        Query(
            query=keyword,
            options=QueryOptions(
                locations=[location],
                limit=25,
                filters=QueryFilters(
                    relevance=RelevanceFilters.RECENT,
                    time=TimeFilters.MONTH,
                    type=[TypeFilters.FULL_TIME],
                    experience=[ExperienceLevelFilters.MID_SENIOR, ExperienceLevelFilters.DIRECTOR, ExperienceLevelFilters.EXECUTIVE],
                    on_site_or_remote=[
                        OnSiteOrRemoteFilters.ON_SITE,
                        OnSiteOrRemoteFilters.REMOTE,
                        OnSiteOrRemoteFilters.HYBRID
                    ]
                )
            )
        )
        for keyword in query_keywords
        for location in locations
    ]

    print(f"🔍 LI_AT_COOKIE = {LI_AT[:10]}... (ocultada)")
    print(f"⏳ Ejecutando {len(queries)} queries a LinkedIn...\n")

    scraper.run(queries)

    end_time = time.time()
    elapsed_minutes = (end_time - start_time) / 60

    print(f"\n✅ Scraping completado. Total de vacantes procesadas: {len(results)}\n")
    print(f"⏱ Tiempo total de scraping: {elapsed_minutes:.2f} minutos")


def extract_modality(insights_list):
    if not insights_list:
        return None
    insights = ' '.join(insights_list).lower()
    if 'remote' in insights:
        return 'Remote'
    elif 'hybrid' in insights:
        return 'Hybrid'
    elif 'on-site' in insights or 'on site' in insights:
        return 'On-site'
    return None
