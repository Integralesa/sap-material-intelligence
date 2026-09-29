"""
Material Intelligence Agent - Main Entry Point
Agente de IA para validación de Master Data en SAP
"""

import os
import json
from dotenv import load_dotenv
from agent.core import MaterialIntelligenceAgent

# Cargar variables de entorno
load_dotenv()

def main():
    """Ejemplo de uso del agente"""

    print("=" * 60)
    print("Material Intelligence Agent - Demo")
    print("=" * 60)
    print()

    # Inicializar agente para Argentina
    agent = MaterialIntelligenceAgent(country="argentina")

    # Ejemplo 1: Validar un material
    print("📋 EJEMPLO 1: Validar Material (Argentina)")
    print("-" * 60)

    material_data = {
        "code": "MAT-CHOC-001",
        "description": "Chocolate Premium Dark 70%",
        "supplier_cuit": "20-12345678-9",
        "supplier_name": "Choco Industries SA",
        "unit": "KG",
        "weight": 500,
        "classification": "FOOD",
        "category": "Alimentos",
        "country_origin": "Argentina"
    }

    print(f"Validando material: {material_data['description']}")
    print()

    result = agent.validate(material_data)

    print(f"Estado: {result['status']}")
    print()

    if result['errors']:
        print("❌ Errores encontrados:")
        for error in result['errors']:
            print(f"  • {error}")
        print()

    if result['warnings']:
        print("⚠️  Advertencias:")
        for warning in result['warnings']:
            print(f"  • {warning}")
        print()

    if result['suggestions']:
        print("💡 Sugerencias:")
        for suggestion in result['suggestions']:
            print(f"  • {suggestion}")
        print()

    # Ejemplo 2: Buscar duplicados
    print()
    print("🔍 EJEMPLO 2: Detectar Duplicados")
    print("-" * 60)

    duplicates = agent.find_duplicates(
        description="Chocolate",
        country="argentina"
    )

    print(f"Búsqueda: Materiales similares a 'Chocolate'")
    print(f"Encontrados: {len(duplicates)}")

    if duplicates:
        for dup in duplicates[:3]:  # Mostrar top 3
            print(f"  • {dup['code']} - {dup['description']} ({dup['match']}% similitud)")
    print()

    # Ejemplo 3: Explicación de campo
    print()
    print("📚 EJEMPLO 3: Educación - Explicar Campo")
    print("-" * 60)

    field_name = "supplier_cuit"
    explanation = agent.explain_field(field_name, country="argentina")

    print(f"Campo: {field_name}")
    print()
    print(explanation)
    print()

    # Ejemplo 4: Validación por lotes
    print()
    print("📦 EJEMPLO 4: Validación por Lotes")
    print("-" * 60)

    materials = [
        {
            "code": "MAT-001",
            "description": "Producto A",
            "supplier_cuit": "20-11111111-1",
            "unit": "KG"
        },
        {
            "code": "MAT-002",
            "description": "Producto B",
            "supplier_cuit": "INVALID",
            "unit": "UN"
        },
        {
            "code": "MAT-003",
            "description": "Producto C",
            "supplier_cuit": "20-33333333-3",
            "unit": "KG"
        }
    ]

    print(f"Validando {len(materials)} materiales...")
    print()

    batch_results = agent.validate_batch(materials)

    approved = sum(1 for r in batch_results if r['status'] == 'APPROVED')
    rejected = sum(1 for r in batch_results if r['status'] == 'REJECTED')

    print(f"✓ Aprobados: {approved}")
    print(f"✗ Rechazados: {rejected}")
    print()

    for result in batch_results:
        status_icon = "✓" if result['status'] == 'APPROVED' else "✗"
        print(f"{status_icon} {result['code']} - {result['status']}")

    print()
    print("=" * 60)
    print("Demo completada")
    print("=" * 60)


def interactive_mode():
    """Modo interactivo para probar el agente"""

    print("Material Intelligence Agent - Modo Interactivo")
    print()

    # Seleccionar país
    print("Selecciona país:")
    print("1. Argentina")
    print("2. Chile")
    print("3. México")

    country_map = {
        "1": "argentina",
        "2": "chile",
        "3": "mexico"
    }

    choice = input("Opción (1-3): ").strip()
    country = country_map.get(choice, "argentina")

    agent = MaterialIntelligenceAgent(country=country)

    while True:
        print()
        print("¿Qué quieres hacer?")
        print("1. Validar material")
        print("2. Buscar duplicados")
        print("3. Explicar campo")
        print("4. Salir")

        option = input("Opción (1-4): ").strip()

        if option == "1":
            print()
            code = input("Código del material: ").strip()
            description = input("Descripción: ").strip()
            cuit = input("CUIT/RUT/RFC: ").strip()

            data = {
                "code": code,
                "description": description,
                "supplier_cuit": cuit,
            }

            result = agent.validate(data)
            print()
            print(f"Resultado: {result['status']}")
            if result['errors']:
                print("Errores:", result['errors'])

        elif option == "2":
            print()
            desc = input("Descripción a buscar: ").strip()
            duplicates = agent.find_duplicates(desc, country)
            print(f"Encontrados: {len(duplicates)}")
            for dup in duplicates[:5]:
                print(f"  • {dup['code']} - {dup['description']}")

        elif option == "3":
            print()
            field = input("Campo a explicar: ").strip()
            explanation = agent.explain_field(field, country)
            print()
            print(explanation)

        elif option == "4":
            print("Adiós!")
            break

        else:
            print("Opción inválida")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        main()
