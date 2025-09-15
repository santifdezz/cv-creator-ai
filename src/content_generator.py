"""
Generador de contenido para CV sin IA (fallback)

Este módulo proporciona funcionalidad para generar contenido de CV
cuando las APIs de IA no están disponibles o fallan.
"""

from typing import Dict, Any, List
import re

class ContentGenerator:
    def __init__(self):
        self.technical_keywords = [
            'python', 'java', 'javascript', 'react', 'node', 'sql', 'html', 'css',
            'angular', 'vue', 'machine learning', 'data', 'analytics', 'programming',
            'backend', 'frontend', 'fullstack', 'api', 'database', 'cloud', 'aws',
            'docker', 'kubernetes', 'git', 'linux', 'mongodb', 'postgresql'
        ]
        
        self.soft_keywords = [
            'liderazgo', 'comunicación', 'teamwork', 'problem solving', 'adaptability',
            'creativity', 'negotiation', 'presentation', 'management', 'leadership',
            'collaboration', 'analytical', 'creative', 'organized', 'proactive'
        ]
        
        self.tools_keywords = [
            'excel', 'powerpoint', 'word', 'photoshop', 'illustrator', 'figma',
            'sketch', 'slack', 'trello', 'jira', 'confluence', 'notion', 'tableau',
            'power bi', 'salesforce', 'hubspot'
        ]

    def generate_fallback_content(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera contenido de CV optimizado sin usar IA externa
        """
        
        # Generar resumen profesional
        resumen = self._generate_professional_summary(form_data)
        
        # Procesar experiencia laboral
        experiencia_optimizada = self._process_work_experience(form_data)
        
        # Organizar habilidades
        habilidades_organizadas = self._organize_skills(form_data)
        
        return {
            "resumen_profesional": resumen,
            "experiencia_optimizada": experiencia_optimizada,
            "habilidades_organizadas": habilidades_organizadas
        }

    def _generate_professional_summary(self, form_data: Dict[str, Any]) -> str:
        """Genera un resumen profesional basado en los datos"""
        
        nombre = form_data.get('nombre', 'Profesional')
        objetivo = form_data.get('objetivo', '')
        experiencia_anos = form_data.get('experiencia_anos', '')
        habilidades = form_data.get('habilidades', '')
        
        # Extraer habilidades principales
        main_skills = []
        if habilidades:
            skills_list = [skill.strip() for skill in habilidades.split(',')[:4]]
            main_skills = [skill for skill in skills_list if skill]
        
        # Plantillas de resumen basadas en experiencia
        if '0-1' in experiencia_anos:
            template = f"Profesional emergente {self._get_field_from_objetivo(objetivo)} con sólida formación académica y pasión por el aprendizaje continuo. Conocimientos en {', '.join(main_skills[:3]) if main_skills else 'múltiples tecnologías'}. Altamente motivado para contribuir al crecimiento organizacional a través de soluciones innovadoras y trabajo colaborativo."
        
        elif '2-3' in experiencia_anos:
            template = f"Profesional con {experiencia_anos.split()[0]} de experiencia {self._get_field_from_objetivo(objetivo)}. Experiencia práctica en {', '.join(main_skills[:3]) if main_skills else 'desarrollo de soluciones'}. Comprometido con la excelencia técnica y el desarrollo de proyectos que generen valor agregado a la organización."
        
        elif '4-5' in experiencia_anos or '6-10' in experiencia_anos:
            template = f"Profesional experimentado con {experiencia_anos.split('-')[0]}+ años de trayectoria {self._get_field_from_objetivo(objetivo)}. Especializado en {', '.join(main_skills[:3]) if main_skills else 'gestión de proyectos complejos'}. Historial comprobado en liderazgo de equipos y optimización de procesos para alcanzar objetivos estratégicos."
        
        elif '10+' in experiencia_anos:
            template = f"Senior profesional con más de 10 años de experiencia {self._get_field_from_objetivo(objetivo)}. Experto en {', '.join(main_skills[:3]) if main_skills else 'dirección estratégica'}. Liderazgo demostrado en transformación digital, gestión de equipos multidisciplinarios y desarrollo de soluciones empresariales de alto impacto."
        
        else:
            # Resumen genérico si no hay información de experiencia
            if objetivo:
                template = f"Profesional versátil especializado en {objetivo}. Competencias sólidas en {', '.join(main_skills[:3]) if main_skills else 'múltiples áreas'} con enfoque en resultados y mejora continua. Comprometido con la innovación y el logro de objetivos organizacionales de manera eficiente."
            else:
                template = f"Profesional multifacético con sólida formación y experiencia práctica. Habilidades diversas en {', '.join(main_skills[:3]) if main_skills else 'análisis, resolución de problemas y comunicación'}. Orientado a resultados con capacidad para adaptarse a entornos dinámicos y contribuir al éxito del equipo."
        
        return template

    def _get_field_from_objetivo(self, objetivo: str) -> str:
        """Extrae el campo profesional del objetivo"""
        if not objetivo:
            return ""
        
        # Buscar patrones comunes
        if any(word in objetivo.lower() for word in ['desarrollador', 'programador', 'software']):
            return "en desarrollo de software"
        elif any(word in objetivo.lower() for word in ['marketing', 'publicidad']):
            return "en marketing digital"
        elif any(word in objetivo.lower() for word in ['datos', 'analytics', 'data']):
            return "en análisis de datos"
        elif any(word in objetivo.lower() for word in ['diseño', 'design', 'ux', 'ui']):
            return "en diseño"
        elif any(word in objetivo.lower() for word in ['ventas', 'comercial']):
            return "en ventas"
        elif any(word in objetivo.lower() for word in ['recursos humanos', 'rrhh']):
            return "en recursos humanos"
        elif any(word in objetivo.lower() for word in ['finanzas', 'contabilidad']):
            return "en finanzas"
        else:
            return f"en {objetivo.lower()[:30]}"

    def _process_work_experience(self, form_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Procesa y optimiza la experiencia laboral"""
        
        experiencia_raw = form_data.get('experiencia_laboral', '')
        if not experiencia_raw:
            return []
        
        experiencia_optimizada = []
        lines = experiencia_raw.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and '-' in line:
                parts = line.split('-', 2)
                if len(parts) >= 2:
                    puesto = parts[0].strip()
                    empresa = parts[1].strip()
                    periodo = parts[2].strip() if len(parts) > 2 else "Período no especificado"
                    
                    # Generar descripciones optimizadas
                    descripciones = self._generate_job_descriptions(puesto, empresa)
                    
                    experiencia_optimizada.append({
                        "puesto": puesto,
                        "empresa": empresa,
                        "periodo": periodo,
                        "descripcion": descripciones
                    })
        
        return experiencia_optimizada

    def _generate_job_descriptions(self, puesto: str, empresa: str) -> List[str]:
        """Genera descripciones optimizadas para un puesto"""
        
        puesto_lower = puesto.lower()
        descripciones = []
        
        # Plantillas basadas en el tipo de puesto
        if any(word in puesto_lower for word in ['desarrollador', 'developer', 'programador']):
            descripciones = [
                "Desarrollé y mantuve aplicaciones web robustas utilizando las mejores prácticas de la industria",
                "Colaboré con equipos multifuncionales para entregar proyectos dentro de los plazos establecidos",
                "Implementé soluciones técnicas que mejoraron la eficiencia del sistema en un 25%"
            ]
        
        elif any(word in puesto_lower for word in ['analista', 'analyst']):
            descripciones = [
                "Analicé datos complejos para identificar tendencias y oportunidades de mejora",
                "Generé reportes ejecutivos que facilitaron la toma de decisiones estratégicas",
                "Optimicé procesos de análisis reduciendo el tiempo de generación de insights en 30%"
            ]
        
        elif any(word in puesto_lower for word in ['gerente', 'manager', 'coordinador']):
            descripciones = [
                "Lideré equipos de trabajo multidisciplinarios alcanzando objetivos organizacionales clave",
                "Implementé estrategias de mejora continua que incrementaron la productividad del equipo",
                "Gestioné recursos y presupuestos optimizando la eficiencia operacional"
            ]
        
        elif any(word in puesto_lower for word in ['diseñador', 'designer']):
            descripciones = [
                "Creé diseños visuales innovadores alineados con la identidad de marca",
                "Colaboré con equipos de desarrollo para implementar interfaces de usuario intuitivas",
                "Mejoré la experiencia del usuario mediante diseños centrados en las necesidades del cliente"
            ]
        
        elif any(word in puesto_lower for word in ['consultor', 'consultant']):
            descripciones = [
                "Asesoré a clientes en la implementación de soluciones estratégicas personalizadas",
                "Realicé diagnósticos organizacionales identificando áreas de mejora y oportunidades",
                "Facilité procesos de cambio organizacional generando valor agregado para los clientes"
            ]
        
        else:
            # Descripciones genéricas pero profesionales
            descripciones = [
                "Ejecuté iniciativas estratégicas que contribuyeron al logro de objetivos organizacionales",
                "Colaboré efectivamente con equipos multidisciplinarios en proyectos de alta prioridad",
                "Implementé mejores prácticas que optimizaron procesos y mejoraron resultados operacionales"
            ]
        
        return descripciones

    def _organize_skills(self, form_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Organiza las habilidades en categorías"""
        
        habilidades_raw = form_data.get('habilidades', '')
        if not habilidades_raw:
            return {"tecnicas": [], "blandas": [], "herramientas": []}
        
        habilidades_list = [skill.strip() for skill in habilidades_raw.split(',') if skill.strip()]
        
        tecnicas = []
        blandas = []
        herramientas = []
        
        for habilidad in habilidades_list:
            habilidad_lower = habilidad.lower()
            categorizada = False
            
            # Verificar habilidades técnicas
            for keyword in self.technical_keywords:
                if keyword in habilidad_lower:
                    tecnicas.append(habilidad)
                    categorizada = True
                    break
            
            if not categorizada:
                # Verificar herramientas
                for keyword in self.tools_keywords:
                    if keyword in habilidad_lower:
                        herramientas.append(habilidad)
                        categorizada = True
                        break
            
            if not categorizada:
                # Verificar habilidades blandas
                for keyword in self.soft_keywords:
                    if keyword in habilidad_lower:
                        blandas.append(habilidad)
                        categorizada = True
                        break
            
            # Si no se puede categorizar, agregar a técnicas por defecto
            if not categorizada:
                tecnicas.append(habilidad)
        
        return {
            "tecnicas": tecnicas,
            "blandas": blandas,
            "herramientas": herramientas
        }