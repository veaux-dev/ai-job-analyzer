'''prompts.py develops the prompts that will be injected to the LLM.'''


def format_vacante(vacante):
    return f"""Título: {vacante['title'].strip()}

Descripción:
{vacante['full_text'].strip()}
"""



def prompt_fit_usuario(vacante):
        return f"""
Eres un asesor experto en búsqueda de empleo para ejecutivos senior en procurement.

Tu cliente es un Director de Procurement con 20 años de experiencia en empresas globales, especializado en sourcing estratégico, manejo de proveedores, negociaciones, lanzamientos de producto y gestión de riesgos. Ha trabajado en los sectores de energía, aeroespacial y automotriz, y domina perfectamente francés, inglés y español.

Tu trabajo es analizar vacantes y decir si **vale la pena que las considere**, desde el punto de vista de su relevancia profesional, impacto potencial y relación con sus competencias principales.

Evalúa la siguiente vacante **solo con base en sus responsabilidades, funciones y enfoque profesional**. No tomes en cuenta el país, idioma o ubicación.

---
Vacante:
{format_vacante(vacante)}
---

¿Crees que esta vacante es un buen match para que este ejecutivo senior en procurement la considere seriamente?

Responde solo con 'sí' o 'no'.
"""

def prompt_procurement(vacante):
    return f"""
Analiza el siguiente texto de una vacante de empleo y determina si la posición está relacionada con procurement, compras, sourcing o gestión de proveedores.

---
{format_vacante(vacante)}
---

Responde solo con 'sí' o 'no'.
"""

def prompt_nivel(vacante):
    return f"""
Analiza esta vacante de empleo y determina su nivel jerárquico principal.

Elige **solo una** de las siguientes opciones:
- entry: si es una posición inicial, de soporte o analista junior
- manager: si lidera procesos o equipos, pero reporta a un director
- director: si lidera una función o equipo regional, reporta a VP
- vp+: si es un rol ejecutivo de dirección general, vicepresidencia, head of global, etc.

---
Título: {vacante['title'].strip()}

Descripción:
{vacante['full_text'].strip()}
---

Responde solo con: entry, manager, director o vp+
"""
