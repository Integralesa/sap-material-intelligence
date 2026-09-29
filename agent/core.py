"""
Core del Material Intelligence Agent
Lógica principal de validación y análisis
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from anthropic import Anthropic

class MaterialIntelligenceAgent:
    """Agente inteligente para validación de Master Data en SAP"""

    def __init__(self, country: str = "argentina"):
        """
        Inicializar agente

        Args:
            country: País (argentina, chile, mexico)
        """
        self.country = country.lower()
        self.client = Anthropic()
        self.conversation_history = []

        # Cargar reglas del país
        self.rules = self._load_country_rules()
        self.sample_materials = self._load_sample_materials()

    def _load_country_rules(self) -> Dict:
        """Cargar reglas de validación por país"""

        rules = {
            "argentina": {
                "required_fields": ["code", "description", "supplier_cuit", "unit"],
                "validations": {
                    "cuit": {
                        "pattern": r"^\d{2}-\d{8}-\d$",
                        "message": "CUIT debe ser XX-XXXXXXXX-X"
                    },
                    "description": {
                        "min_length": 5,
                        "max_length": 100
                    }
                },
                "rules": [
                    "No puede haber tildes en descripción",
                    "CUIT debe ser válido según AFIP",
                    "Unidad debe estar en catálogo SAP",
                    "Material no puede ser duplicado"
                ]
            },
            "chile": {
                "required_fields": ["code", "description", "supplier_rut", "unit"],
                "validations": {
                    "rut": {
                        "pattern": r"^\d{1,2}\.\d{3}\.\d{3}-[0-9K]$",
                        "message": "RUT debe ser XX.XXX.XXX-X"
                    }
                },
                "rules": [
                    "RUT debe validarse con algoritmo SII",
                    "Código regional obligatorio",
                    "Clasificación por actividad económica"
                ]
            },
            "mexico": {
                "required_fields": ["code", "description", "supplier_rfc", "unit"],
                "validations": {
                    "rfc": {
                        "pattern": r"^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$",
                        "message": "RFC debe tener formato correcto"
                    }
                },
                "rules": [
                    "RFC debe validarse con SAT",
                    "Régimen fiscal obligatorio",
                    "CLABE interbancaria requerida"
                ]
            }
        }

        return rules.get(self.country, rules["argentina"])

    def _load_sample_materials(self) -> List[Dict]:
        """Cargar materiales de ejemplo para búsqueda de duplicados"""

        return [
            {
                "code": "MAT-0001",
                "description": "Chocolate Premium Dark",
                "supplier": "Choco Industries",
                "category": "FOOD"
            },
            {
                "code": "MAT-0002",
                "description": "Chocolate con Leche",
                "supplier": "Choco Industries",
                "category": "FOOD"
            },
            {
                "code": "MAT-0003",
                "description": "Chocolate Blanco",
                "supplier": "Sweet Corp",
                "category": "FOOD"
            },
            {
                "code": "MAT-0045",
                "description": "Premium Chocolate Mix",
                "supplier": "Premium Foods",
                "category": "FOOD"
            },
            {
                "code": "MAT-0100",
                "description": "Aceite Vegetal Premium",
                "supplier": "Oil Company",
                "category": "OILS"
            }
        ]

    def validate(self, material_data: Dict) -> Dict:
        """
        Validar un material

        Args:
            material_data: Datos del material a validar

        Returns:
            Dict con status, errors, warnings, suggestions
        """

        errors = []
        warnings = []
        suggestions = []

        # Validar campos requeridos
        for field in self.rules["required_fields"]:
            if field not in material_data or not material_data[field]:
                errors.append(f"Campo requerido faltante: {field}")

        # Validar formato de campos
        for field, validation in self.rules["validations"].items():
            if field in material_data and material_data[field]:
                value = str(material_data[field])

                if "pattern" in validation:
                    if not re.match(validation["pattern"], value):
                        errors.append(f"{field}: {validation['message']}")

                if "min_length" in validation:
                    if len(value) < validation["min_length"]:
                        errors.append(f"{field}: Mínimo {validation['min_length']} caracteres")

                if "max_length" in validation:
                    if len(value) > validation["max_length"]:
                        errors.append(f"{field}: Máximo {validation['max_length']} caracteres")

        # Usar Claude para análisis más profundo
        if self._has_api_key():
            ai_analysis = self._analyze_with_claude(material_data)
            errors.extend(ai_analysis.get("errors", []))
            warnings.extend(ai_analysis.get("warnings", []))
            suggestions.extend(ai_analysis.get("suggestions", []))

        # Determinar status
        status = "APPROVED" if not errors else "REJECTED"

        return {
            "status": status,
            "code": material_data.get("code", "UNKNOWN"),
            "errors": list(set(errors)),  # Remover duplicados
            "warnings": list(set(warnings)),
            "suggestions": list(set(suggestions)),
            "timestamp": datetime.now().isoformat()
        }

    def validate_batch(self, materials: List[Dict]) -> List[Dict]:
        """
        Validar múltiples materiales

        Args:
            materials: Lista de materiales a validar

        Returns:
            Lista de resultados de validación
        """

        results = []
        for material in materials:
            result = self.validate(material)
            results.append(result)

        return results

    def find_duplicates(self, description: str, country: Optional[str] = None) -> List[Dict]:
        """
        Buscar materiales duplicados o similares

        Args:
            description: Descripción del material a buscar
            country: País (opcional, usa país del agente por defecto)

        Returns:
            Lista de materiales similares
        """

        duplicates = []
        description_lower = description.lower()

        for material in self.sample_materials:
            material_desc_lower = material["description"].lower()

            # Cálculo simple de similitud
            match_score = self._similarity_score(description_lower, material_desc_lower)

            if match_score >= 0.6:  # 60% de similitud mínima
                duplicates.append({
                    "code": material["code"],
                    "description": material["description"],
                    "supplier": material.get("supplier", "Unknown"),
                    "category": material.get("category", "Unknown"),
                    "match": int(match_score * 100)
                })

        # Ordenar por similitud
        duplicates.sort(key=lambda x: x["match"], reverse=True)

        return duplicates

    def explain_field(self, field_name: str, country: Optional[str] = None) -> str:
        """
        Explicar la importancia de un campo

        Args:
            field_name: Nombre del campo a explicar
            country: País (opcional)

        Returns:
            Explicación detallada del campo
        """

        explanations = {
            "supplier_cuit": "CUIT es el Código Único de Identificación Tributaria. Es crítico porque: (1) Sin CUIT válido no puedes facturar, (2) Datos incorrectos generan rechazos en AFIP, (3) Es requerido para cualquier transacción comercial. Formato: XX-XXXXXXXX-X",

            "supplier_rut": "RUT es el Rol Único Tributario de Chile. Importancia: (1) Validación con algoritmo SII es obligatoria, (2) RUT inválido bloquea pagos, (3) Afecta reportes de tributación. Formato: XX.XXX.XXX-X",

            "supplier_rfc": "RFC es el Registro Federal de Contribuyentes en México. Por qué importa: (1) Identificador único ante SAT, (2) RFC inválido impide facturación, (3) Afecta comprobantes fiscales. Validación con SAT es obligatoria.",

            "description": "Descripción es el nombre del material que ven todos. Importancia: (1) Usuarios buscan por descripción, (2) Si es confusa hay duplicados, (3) Debe ser clara y única. Máximo 100 caracteres sin tildes.",

            "code": "Código es el identificador único del material. Crítico porque: (1) No puede repetirse, (2) Usuarios lo buscan primero, (3) Base para auditoría. Debe ser alfanumérico y único.",

            "unit": "Unidad de medida. Importancia: (1) Define cómo se compra/vende, (2) Si es incorrecta el precio está mal, (3) Afecta all transacciones. Debe estar en catálogo SAP.",
        }

        return explanations.get(
            field_name,
            f"Campo: {field_name}. No hay documentación específica. Verifica en tu proceso de negocio."
        )

    def _analyze_with_claude(self, material_data: Dict) -> Dict:
        """Análisis profundo usando Claude API"""

        try:
            prompt = f"""
Analiza este material de SAP para validación:

País: {self.country}
Datos: {json.dumps(material_data, indent=2)}

Verifica:
1. Errores críticos (qué evitaría procesamiento)
2. Advertencias (qué causaría rechazo después)
3. Sugerencias de mejora

Responde en JSON:
{{
    "errors": ["error1", "error2"],
    "warnings": ["warning1"],
    "suggestions": ["suggestion1"]
}}
"""

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Parsear respuesta JSON
            response_text = message.content[0].text

            # Extraer JSON de la respuesta
            start = response_text.find('{')
            end = response_text.rfind('}') + 1

            if start >= 0 and end > start:
                json_str = response_text[start:end]
                return json.loads(json_str)

            return {"errors": [], "warnings": [], "suggestions": []}

        except Exception as e:
            print(f"Error en análisis Claude: {e}")
            return {"errors": [], "warnings": [], "suggestions": []}

    def _similarity_score(self, str1: str, str2: str) -> float:
        """Calcular similitud entre dos strings (0-1)"""

        # Algoritmo simple: qué porcentaje de palabras coinciden
        words1 = set(str1.split())
        words2 = set(str2.split())

        if not words1 or not words2:
            return 0.0

        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        return intersection / union if union > 0 else 0.0

    def _has_api_key(self) -> bool:
        """Verificar si hay API key disponible"""
        return bool(os.getenv("ANTHROPIC_API_KEY"))

    def generate_report(self, results: List[Dict]) -> str:
        """Generar reporte de validaciones"""

        total = len(results)
        approved = sum(1 for r in results if r["status"] == "APPROVED")
        rejected = total - approved

        report = f"""
REPORTE DE VALIDACIÓN DE MATERIALES
País: {self.country.upper()}
Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
{'='*50}

RESUMEN:
- Total validados: {total}
- Aprobados: {approved} ({int(approved/total*100) if total > 0 else 0}%)
- Rechazados: {rejected} ({int(rejected/total*100) if total > 0 else 0}%)

DETALLES:
"""

        for result in results:
            report += f"\n{result['code']}: {result['status']}"
            if result['errors']:
                for error in result['errors'][:2]:
                    report += f"\n  ✗ {error}"

        return report


if __name__ == "__main__":
    # Test básico
    agent = MaterialIntelligenceAgent(country="argentina")

    test_material = {
        "code": "TEST-001",
        "description": "Test Material",
        "supplier_cuit": "20-12345678-9",
        "unit": "KG"
    }

    result = agent.validate(test_material)
    print(f"Test: {result['status']}")
