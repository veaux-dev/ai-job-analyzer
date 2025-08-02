from modules.classifier import extraer_info_empresa

empresa = input("Nombre de la empresa: ").strip()

info = extraer_info_empresa(empresa)


if not info:
    print("❌ No se pudo obtener información.")
else:
    print("\n📊 Resultado de análisis:\n")
    print(f"🏢 Empresa          : {info['company']}")
    print(f"📝 Resumen         : {info['resumen_empresa']}")
    print(f"🏭 Sector           : {info['sector_empresa']}")
    print(f"📦 Tamaño           : {info['tamaño_empresa']}")
    print(f"🇲🇽 Presencia en MX : {info['presencia_mexico']}")
    print(f"🌟 Glassdoor Score  : {info['glassdoor_score'] if info['glassdoor_score'] else 'Sin información'}")
    print(f"📅 Última revisión  : {info['last_updated']}")