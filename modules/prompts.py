'''prompts.py develops the prompts that will be injected to the LLM.'''


def format_vacante(vacante):
    return f"""Título: {vacante['title'].strip()}

Descripción:
{vacante['full_text'].strip()}
"""



def prompt_fit_usuario(vacante):
    return f"""
You are a job search advisor specialized in helping senior procurement executives.

Your client is a Procurement Director with 20 years of experience in global companies. His expertise includes strategic sourcing, supplier management, category management, contract negotiations, procurement involvement in product launches (NPI), and supplier/supply risk mitigation. He has worked in the energy, aerospace, and automotive sectors, and is fluent in French, English, and Spanish.

Your job is to assess job postings and determine whether they are **truly worth considering** based on their professional relevance, potential impact, and alignment with your client's core strengths.

Focus your evaluation **only on the responsibilities, main functions, and core focus of the role**. Ignore the country, language, or location.

⚠️ Important:
- Only answer 'yes' if the role includes **direct responsibility over procurement, strategic sourcing, or supplier management**.
- Do NOT answer 'yes' if the role only interacts with those areas but is primarily focused on engineering, product, manufacturing, or general operations.
- Ignore surface-level mentions like “collaborates with sourcing” or “supports procurement” if the role is not directly accountable for those functions.

---
Job posting:
{format_vacante(vacante)}
---

Do you believe this job is a good match for this senior procurement executive to seriously consider?

Reply with only 'yes' or 'no'.
"""

def prompt_procurement(vacante):
    return f"""
Analiza el siguiente texto de una vacante de empleo y determina si la posición está primeramente y principalmente de procurement, compras estrategicas, sourcing o gestión de proveedores.
Si la posicion no cumple con la descripcion anterior, no dudes en descartarla. Busco FUERTE correlacion donde el candidato ideal es un profesional en el area.

---
{format_vacante(vacante)}
---

Responde solamente con 'sí' o 'no'. 
"""

def prompt_nivel(vacante):
    return f"""
Analiza esta vacante de empleo y determina su nivel jerárquico principal.

Elige **solo una** de las siguientes opciones, si no esta claro, pon '0-unclear':
- 1-entry: por entry level. Si es una posición inicial, tipicamente menos de 5 anos de experiencia requeridad. individual contributor. Soporte o analista junior
- 2-experienced: seguimos en posicines de individual contributor (sin reportes) pero ya para gente mas experimientada 
- 3-manager: lider de equipo, pero reporta a un director
- 4-director: si lidera una función o equipo regional, reporta a VP
- 5-vp+: si es un rol ejecutivo de dirección general, vicepresidencia, head of global, etc.

Llega a la conclusion del nivel usando el titulo del puesto y la descripcion. No dudes en castigar niveles si no estas seguro.

---
Título: {vacante['title'].strip()}

Descripción:
{vacante['full_text'].strip()}
---

Responde solo con: 0-unclear, 1-entry, 2-experienced, 3-manager, 4-director o 5-vp+
"""
def prompt_info_empresa(nombre_empresa):
    return f"""
Quiero que actúes como un analista de empresas con alto criterio profesional.

Tu tarea es analizar la empresa "{nombre_empresa}" y devolver únicamente información verificada o comúnmente conocida. 
Si no estás seguro o no tienes suficiente información para responder con confianza, escribe "Sin información" en ese campo.

Necesito los siguientes datos en formato JSON:

- resumen_empresa: resumen breve (1–3 líneas) de lo que hace la empresa
- sector_empresa: el giro principal o industria (ej. aeroespacial, tecnología, logística…)
- tamaño_empresa: pequeña, mediana, grande o multinacional
- presencia_mexico: Sí / No / Parcial / Sin información
- glassdoor_score: número de 1.0 a 5.0 si lo conoces, o "Sin información"

Ejemplo de salida esperada:

{{
  "resumen_empresa": "Empresa francesa especializada en motores aeronáuticos y defensa.",
  "sector_empresa": "Aeroespacial",
  "tamaño_empresa": "Multinacional",
  "presencia_mexico": "Sí",
  "glassdoor_score": 3.9
}}

Si no tienes información clara, responde con "Sin información". No inventes.
"""    