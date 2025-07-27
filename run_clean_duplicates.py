from modules.db_vacantes import fetch_all_vacantes, calculate_hash
import sqlite3
from collections import defaultdict

def normalize_link(link):
    return link.split('?')[0].strip()

def cleanup_duplicates_normalized_links():
    print("🔧 Iniciando limpieza de duplicados con normalización de links…")

    rows = fetch_all_vacantes()
    seen_hashes = set()
    deleted = 0

    conn = sqlite3.connect("vacantes.db")
    cursor = conn.cursor()

    for row in rows:
        old_hash = row[0]
        link = row[9]  # campo 'link'

        norm_link = normalize_link(link)
        new_hash = calculate_hash({"link": norm_link})

        if new_hash in seen_hashes:
            cursor.execute("DELETE FROM vacantes WHERE job_hash = ?", (old_hash,))
            deleted += 1
        else:
            if old_hash != new_hash:
                cursor.execute("""
                    UPDATE vacantes
                    SET job_hash = ?, link = ?
                    WHERE job_hash = ?
                """, (new_hash, norm_link, old_hash))
            seen_hashes.add(new_hash)

    conn.commit()
    conn.close()
    print(f"✔ Limpieza completada. Registros eliminados: {deleted}")

if __name__ == "__main__":
    cleanup_duplicates_normalized_links()
