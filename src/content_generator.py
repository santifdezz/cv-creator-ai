"""
Generador de contenido para CV sin IA (fallback)

Este módulo proporciona funcionalidad para generar contenido de CV
cuando las APIs de IA no están disponibles o fallan.
"""

from typing import Dict, Any, List
import re

class ContentGenerator:
    def __init__(self):
        # Palabras clave ATS por sector (expandidas)
        self.ats_keywords = {
            "tech": [
                "JavaScript", "Python", "React", "Node.js", "SQL", "Git", "Docker", "AWS", 
                "Agile", "Scrum", "API", "REST", "Microservices", "CI/CD", "DevOps",
                "Machine Learning", "Data Analysis", "Problem Solving", "Team Leadership",
                "Full Stack", "Frontend", "Backend", "Database Management", "Cloud Computing",
                "TypeScript", "MongoDB", "PostgreSQL", "Redis", "Kubernetes", "Jenkins",
                "HTML5", "CSS3", "Vue.js", "Angular", "Express.js", "GraphQL", "NoSQL",
                "TDD", "Unit Testing", "Integration Testing", "Performance Optimization"
            ],
            "marketing": [
                "Digital Marketing", "SEO", "SEM", "Social Media", "Content Strategy",
                "Analytics", "Google Analytics", "Campaign Management", "Lead Generation",
                "Brand Management", "Market Research", "Email Marketing", "CRM",
                "ROI Optimization", "A/B Testing", "Customer Acquisition", "PPC",
                "Content Creation", "Influencer Marketing", "Marketing Automation",
                "Conversion Rate Optimization", "Customer Journey Mapping", "KPI Analysis"
            ],
            "sales": [
                "Sales Management", "Lead Generation", "Customer Relationship Management",
                "CRM", "Pipeline Management", "Revenue Growth", "Account Management",
                "Negotiation", "Closing Deals", "B2B Sales", "B2C Sales", "Prospecting",
                "Sales Forecasting", "Territory Management", "Key Account Management",
                "Consultative Selling", "Solution Selling", "Customer Retention"
            ],
            "design": [
                "UI Design", "UX Design", "User Experience", "User Interface", "Figma",
                "Adobe Creative Suite", "Photoshop", "Illustrator", "Sketch", "InVision",
                "Wireframing", "Prototyping", "User Research", "Design Thinking",
                "Visual Design", "Interaction Design", "Information Architecture"
            ],
            "general": [
                "Project Management", "Leadership", "Communication", "Problem Solving",
                "Team Collaboration", "Strategic Planning", "Process Improvement",
                "Data Analysis", "Customer Service", "Time Management", "Adaptability",
                "Innovation", "Critical Thinking", "Results-Oriented", "Multi-tasking",
                "Cross-functional Collaboration", "Stakeholder Management", "Budget Management"
            ]
        }
        
        # Plantillas mejoradas con optimización ATS
        self.enhanced_templates = {
            "tech": {
                "summary": """Desarrollador {experience_level} con {years}+ años de experiencia especializado en {tech_skills} y arquitecturas escalables. Expertise comprobado en metodologías Agile/Scrum, desarrollo Full Stack y implementación de soluciones cloud-native. Historial demostrado de liderazgo técnico, optimización de rendimiento y entrega de proyectos de alto impacto en equipos multidisciplinarios.""",
                
                "experience_bullets": [
                    "Desarrollé y mantuve aplicaciones web escalables utilizando {tech_stack}, mejorando el rendimiento del sistema en un 40% y reduciendo los tiempos de carga",
                    "Implementé arquitecturas de microservicios y APIs RESTful, optimizando la escalabilidad y facilitando la integración con sistemas externos",
                    "Lideré equipos de desarrollo en metodologías Agile/Scrum, coordinando sprints, daily standups y retrospectivas para maximizar la productividad",
                    "Aplicé principios de DevOps incluyendo CI/CD pipelines, containerización con Docker y despliegue automatizado en plataformas cloud",
                    "Mentoricé a desarrolladores junior, establecí estándares de código y lideré code reviews para mantener alta calidad del software"
                ]
            },
            
            "marketing": {
                "summary": """Especialista en Marketing Digital con {years}+ años de experiencia en estrategias de crecimiento y optimización ROI. Expertise en SEO/SEM, Social Media Marketing y análisis avanzado de datos con Google Analytics. Historial comprobado de incremento de conversiones (+35%), generación de leads cualificados y gestión exitosa de presupuestos de marketing. Experiencia en liderazgo de equipos creativos y colaboración cross-funcional.""",
                
                "experience_bullets": [
                    "Desarrollé e implementé estrategias de marketing digital omnicanal que incrementaron el tráfico orgánico en un 60% y las conversiones en un 35%",
                    "Gestioné campañas de SEM y Social Media Advertising con presupuestos de €75K+, optimizando el ROAS y reduciendo el CPA en un 25%",
                    "Realicé análisis profundo de mercado y segmentación de audiencias para optimizar el targeting y personalizar el customer journey",
                    "Implementé sistemas de marketing automation y lead scoring que mejoraron la calificación de leads en un 40%",
                    "Colaboré con equipos de ventas y producto para alinear estrategias go-to-market y optimizar el funnel de conversión"
                ]
            },
            
            "sales": {
                "summary": """Profesional de Ventas con {years}+ años de experiencia en gestión de cuentas clave y desarrollo de nuevos mercados. Expertise en consultative selling, negociación estratégica y gestión de pipeline. Historial comprobado de superación de objetivos de ventas (+120% quota achievement), retención de clientes y crecimiento de revenue. Experiencia en CRM management y análisis de métricas de ventas.""",
                
                "experience_bullets": [
                    "Gestioné cartera de cuentas clave generando €2M+ en revenue anual, manteniendo una tasa de retención del 95%",
                    "Desarrollé nuevos territorios de venta identificando oportunidades de mercado y estableciendo relaciones estratégicas con stakeholders",
                    "Implementé procesos de sales enablement y metodologías consultivas que incrementaron la tasa de cierre en un 30%",
                    "Colaboré con equipos de marketing para optimizar lead generation y desarrollar contenido de apoyo a ventas",
                    "Mentoricé a sales representatives junior y establecí best practices para accelerar el ciclo de ventas"
                ]
            }
        }

    def detect_sector(self, experience_text: str, skills_text: str, objective_text: str = "") -> str:
        """Detecta el sector profesional basado en experiencia, habilidades y objetivo"""
        text = f"{experience_text} {skills_text} {objective_text}".lower()
        
        sector_indicators = {
            "tech": ["programador", "desarrollador", "software", "web", "javascript", "python", 
                    "react", "api", "backend", "frontend", "fullstack", "devops", "coding"],
            "marketing": ["marketing", "publicidad", "seo", "sem", "social media", "campañas", 
                         "digital", "brand", "content", "analytics", "roi"],
            "sales": ["ventas", "comercial", "account", "cliente", "negociación", "revenue", 
                     "pipeline", "crm", "prospecting"],
            "design": ["diseño", "design", "ux", "ui", "figma", "photoshop", "illustrator", 
                      "creative", "visual", "wireframe", "prototype"]
        }
        
        sector_scores = {}
        for sector, indicators in sector_indicators.items():
            score = sum(1 for indicator in indicators if indicator in text)
            sector_scores[sector] = score
        
        detected_sector = max(sector_scores, key=sector_scores.get)
        return detected_sector if sector_scores[detected_sector] > 0 else "general"

    def enhance_with_ats_keywords(self, text: str, sector: str) -> str:
        """Mejora el texto añadiendo palabras clave ATS relevantes de forma natural"""
        if not text:
            return text
            
        keywords = self.ats_keywords.get(sector, self.ats_keywords["general"])
        
        # Convierte texto a lista de palabras para análisis
        words_in_text = text.lower().split()
        
        # Encuentra keywords relevantes que no están en el texto
        relevant_keywords = []
        for keyword in keywords[:8]:  # Toma las 8 más relevantes
            if not any(word in keyword.lower() for word in words_in_text):
                relevant_keywords.append(keyword)
        
        # Si el texto es corto, añade keywords naturalmente
        if len(text.split()) < 30 and relevant_keywords:
            enhanced_text = f"{text} Competencias destacadas: {', '.join(relevant_keywords[:4])}."
            return enhanced_text
        
        return text

    def _calculate_years_experience(self, experience_text: str) -> int:
        """Calcula años de experiencia basado en el texto de experiencia"""
        if not experience_text:
            return 1
            
        # Busca patrones de fechas
        year_pattern = r'\b(20\d{2})\b'
        years = re.findall(year_pattern, experience_text)
        
        if len(years) >= 2:
            years = [int(y) for y in years]
            return max(years) - min(years)
        
        # Fallback: estima basado en cantidad de trabajos
        jobs = experience_text.split('\n')
        job_count = len([job for job in jobs if job.strip()])
        return min(job_count * 2, 8)  # Max 8 años estimados

    def generate_enhanced_cv_content(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Genera contenido de CV optimizado para ATS con detección inteligente de sector"""
        
        # Detecta el sector profesional
        sector = self.detect_sector(
            form_data.get('experiencia_laboral', ''), 
            form_data.get('habilidades', ''),
            form_data.get('objetivo', '')
        )
        
        # Calcula años de experiencia
        years = self._calculate_years_experience(form_data.get('experiencia_laboral', ''))
        
        # Genera contenido usando plantillas específicas del sector
        if sector in self.enhanced_templates:
            template = self.enhanced_templates[sector]
            
            # Determina nivel de experiencia
            if years >= 7:
                experience_level = "Senior"
            elif years >= 3:
                experience_level = "Mid-level"
            else:
                experience_level = "Junior"
            
            # Genera resumen profesional optimizado
            summary = template["summary"].format(
                experience_level=experience_level,
                years=years,
                tech_skills=form_data.get('habilidades', 'tecnologías modernas')[:50],
                tech_stack=form_data.get('habilidades', 'stack tecnológico actual')[:40]
            )
            
            # Procesa experiencia laboral con bullets optimizados
            experience_bullets = template.get("experience_bullets", [])
            enhanced_experience = self._enhance_experience_with_bullets(
                form_data.get('experiencia_laboral', ''), 
                experience_bullets,
                form_data.get('habilidades', '')
            )
            
        else:
            # Fallback al método original mejorado
            summary = self._generate_enhanced_summary(form_data, sector, years)
            enhanced_experience = self._process_work_experience(form_data)
        
        # Optimiza habilidades con keywords ATS
        enhanced_skills = self._optimize_skills_for_ats(
            form_data.get('habilidades', ''), sector
        )
        
        return {
            'resumen_profesional': summary,
            'experiencia_optimizada': enhanced_experience,
            'habilidades_organizadas': enhanced_skills,
            'sector_detectado': sector,
            'nivel_experiencia': f"{years} años"
        }

    def _enhance_experience_with_bullets(self, original_experience: str, bullet_templates: List[str], skills: str) -> List[Dict[str, Any]]:
        """Mejora la experiencia laboral usando bullets optimizados para ATS"""
        if not original_experience:
            return []
        
        jobs = original_experience.split('\n')
        enhanced_jobs = []
        
        for job in jobs:
            if not job.strip():
                continue
                
            # Extrae información básica del trabajo
            parts = job.split(' - ')
            if len(parts) >= 3:
                position = parts[0].strip()
                company = parts[1].strip()
                period = parts[2].strip()
                
                # Selecciona bullets aleatorios y los personaliza
                selected_bullets = bullet_templates[:3] if bullet_templates else []
                personalized_bullets = []
                
                for bullet in selected_bullets:
                    # Personaliza el bullet con habilidades del usuario
                    tech_skills = skills.split(',')[:3] if skills else ['tecnologías modernas']
                    formatted_bullet = bullet.format(
                        tech_stack=', '.join([s.strip() for s in tech_skills])
                    )
                    personalized_bullets.append(formatted_bullet)
                
                enhanced_jobs.append({
                    "puesto": position,
                    "empresa": company,
                    "periodo": period,
                    "descripcion": personalized_bullets
                })
        
        return enhanced_jobs

    def _optimize_skills_for_ats(self, skills_text: str, sector: str) -> Dict[str, List[str]]:
        """Optimiza y categoriza las habilidades añadiendo keywords ATS relevantes"""
        
        # Obtiene keywords del sector
        sector_keywords = self.ats_keywords.get(sector, self.ats_keywords["general"])
        
        # Procesa habilidades del usuario
        user_skills = []
        if skills_text:
            user_skills = [s.strip() for s in skills_text.split(',') if s.strip()]
        
        # Categoriza habilidades
        technical_skills = []
        soft_skills = []
        tools_skills = []
        
        # Palabras clave para categorización
        tech_indicators = ["javascript", "python", "react", "sql", "api", "cloud", "docker", "programming"]
        soft_indicators = ["leadership", "communication", "teamwork", "management", "analytical"]
        tools_indicators = ["excel", "photoshop", "figma", "jira", "salesforce", "analytics"]
        
        # Categoriza habilidades existentes
        for skill in user_skills:
            skill_lower = skill.lower()
            if any(indicator in skill_lower for indicator in tech_indicators):
                technical_skills.append(skill)
            elif any(indicator in skill_lower for indicator in soft_indicators):
                soft_skills.append(skill)
            elif any(indicator in skill_lower for indicator in tools_indicators):
                tools_skills.append(skill)
            else:
                technical_skills.append(skill)  # Default a técnicas
        
        # Añade keywords ATS relevantes
        for keyword in sector_keywords:
            keyword_lower = keyword.lower()
            
            # Evita duplicados
            if not any(keyword_lower in existing.lower() for existing in technical_skills + soft_skills + tools_skills):
                if any(indicator in keyword_lower for indicator in tech_indicators):
                    technical_skills.append(keyword)
                elif any(indicator in keyword_lower for indicator in soft_indicators):
                    soft_skills.append(keyword)
                elif any(indicator in keyword_lower for indicator in tools_indicators):
                    tools_skills.append(keyword)
                else:
                    technical_skills.append(keyword)
        
        # Limita el número de habilidades por categoría
        return {
            "tecnicas": technical_skills[:8],
            "blandas": soft_skills[:5],
            "herramientas": tools_skills[:5]
        }

    def _generate_enhanced_summary(self, form_data: Dict[str, Any], sector: str, years: int) -> str:
        """Genera un resumen profesional mejorado como fallback"""
        name = form_data.get('nombre', 'Profesional')
        experience_level = "Senior" if years >= 7 else "Mid-level" if years >= 3 else "Junior"
        
        sector_titles = {
            "tech": "Desarrollador",
            "marketing": "Especialista en Marketing", 
            "sales": "Profesional de Ventas",
            "design": "Diseñador",
            "general": "Profesional"
        }
        
        title = sector_titles.get(sector, "Profesional")
        
        summary = f"""{title} {experience_level} con {years}+ años de experiencia demostrada en {sector}. 
        Expertise en resolución de problemas complejos, liderazgo de equipos y entrega de resultados excepcionales. 
        Historial comprobado de mejora de procesos, optimización de rendimiento y colaboración cross-funcional 
        en entornos dinámicos y orientados a resultados."""
        
        # Añade keywords ATS naturalmente
        return self.enhance_with_ats_keywords(summary, sector)

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