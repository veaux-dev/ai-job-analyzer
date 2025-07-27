from modules.db_vacantes import fetch_all_vacantes, update_vacante_fields
from modules.prompts import prompt_procurement, prompt_fit_usuario, prompt_nivel
from modules.tu_llm_wrapper import evaluar_booleano, evaluar_con_llm
from datetime import datetime

DEFAULT_MODEL = 'gemma3'

def es_procurement(vacante):
    if not vacante['full_text'].strip():
        return None
    return evaluar_booleano(prompt_procurement(vacante), modelo=DEFAULT_MODEL)

def es_fit_usuario(vacante):
    if not vacante['full_text'].strip():
        return None
    return evaluar_booleano(prompt_fit_usuario(vacante), modelo=DEFAULT_MODEL)

def estimar_nivel(vacante):
    if not vacante['full_text'].strip():
        return None
    nivel = evaluar_con_llm(prompt_nivel(vacante), modelo=DEFAULT_MODEL).strip().lower()
    if nivel in ['entry', 'manager', 'director', 'vp+']:
        return nivel
    return None

def clasificar_vacantes():
    vacantes = fetch_all_vacantes()
    print(f"🧠 Clasificando {len(vacantes)} vacantes...")

    for vac in vacantes:
        id_ = vac['job_hash']
        cambios = {}

        # Paso 1: ¿Es procurement?
        if vac['es_procurement'] is None:
            cambios['es_procurement'] = es_procurement(vac)
            print(f"[{id_}] es_procurement: {cambios['es_procurement']}")

        # Paso 2: Si es procurement, evaluar si es fit
        if cambios.get('es_procurement') or vac['es_procurement']:
            if vac['es_fit_usuario'] is None:
                cambios['es_fit_usuario'] = es_fit_usuario(vac)
                print(f"[{id_}] es_fit_usuario: {cambios['es_fit_usuario']}")

        # Paso 3: Estimar nivel
        if vac['nivel_estimado'] is None:
            cambios['nivel_estimado'] = estimar_nivel(vac)
            print(f"[{id_}] nivel_estimado: {cambios['nivel_estimado']}")

        # Si hubo clasificación por LLM, registra fecha
        if any(k in cambios for k in ['es_procurement', 'es_fit_usuario', 'nivel_estimado']):
            cambios['processed_at'] = datetime.today().strftime('%Y-%m-%d')

        if cambios:
            update_vacante_fields(id_, cambios)
