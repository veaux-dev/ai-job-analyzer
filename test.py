from modules.tu_llm_wrapper import evaluar_booleano, evaluar_con_llm
from modules.classifier import prompt_fit_usuario,prompt_procurement

texto = """
We are hiring a Director of Business Operations for Global Programs.

This role involves driving operational efficiency across multiple business units by aligning vendor strategies, optimizing supplier performance, and leading cross-functional sourcing initiatives.

The position owns several global RFx cycles per year and works closely with procurement, legal, finance, and engineering teams to ensure supplier compliance and risk mitigation.

Experience in strategic sourcing, supplier negotiations, and contract lifecycle management is essential.
"""

# Prueba procurement
prompt1 = prompt_procurement(texto)
print("¿Es procurement?", evaluar_booleano(prompt1, modelo='gemma3'))

# Prueba fit con tu perfil
prompt2 = prompt_fit_usuario(texto)
print("¿Es fit con mi perfil?", evaluar_booleano(prompt2, modelo='gemma3'))
print("¿Es fit con mi perfil?", evaluar_con_llm(prompt2, modelo='gemma3'))

