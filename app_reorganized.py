import gradio as gr
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import logging
import traceback
import tempfile
import shutil

# Importar nuestros módulos
from src.ai_service import AIService
from src.content_generator import ContentGenerator  
from src.pdf_generator import PDFGenerator
from src.config import API_CONFIGS
from src.utils import validate_email, validate_phone, validate_linkedin, clean_text

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CVGeneratorApp:
    """Aplicación principal para generar CVs con IA"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.content_generator = ContentGenerator()
        self.pdf_generator = PDFGenerator()
        
        # Estado de autoguardado
        self.autosave_enabled = True
        self.autosave_data = {}
        
    def create_interface(self):
        """Crear la interfaz de Gradio optimizada y reorganizada"""
        
        with gr.Blocks(
            theme=gr.themes.Soft(
                primary_hue="blue",
                secondary_hue="gray", 
                neutral_hue="slate"
            ),
            title="🚀 CV Creator AI - Generador Profesional de CVs",
            css=self.get_custom_css()
        ) as demo:
            
            # Header principal
            gr.HTML("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; text-align: center; margin: -1rem -1rem 2rem -1rem; border-radius: 0 0 20px 20px;">
                <h1 style="color: white; font-size: 3rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                    🚀 <strong>CV Creator AI</strong>
                </h1>
                <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin-top: 0.5rem; margin-bottom: 0;">
                    ✨ Genera CVs profesionales optimizados para ATS con Inteligencia Artificial
                </p>
            </div>
            """)
            
            # Contenido principal reorganizado para mejor UX (3 columnas equitativas)
            with gr.Row(equal_height=False):
                # ===================================================================
                # COLUMNA 1: INFORMACIÓN PERSONAL + CONFIGURACIÓN IA (33%)
                # ===================================================================
                with gr.Column(scale=1, min_width=320):
                    gr.Markdown("## 👤 **Información Personal**")
                    
                    # Información básica
                    with gr.Group():
                        gr.Markdown("### ✨ **Datos Básicos** *(Obligatorio)*")
                        
                        nombre = gr.Textbox(
                            label="Nombre Completo *",
                            placeholder="Ej: María García López",
                            info="Tu nombre completo como aparecerá en el CV",
                            lines=1,
                            elem_id="nombre_input"
                        )
                        
                        email = gr.Textbox(
                            label="Email *",
                            placeholder="maria.garcia@email.com",
                            info="Email profesional preferiblemente",
                            lines=1,
                            elem_id="email_input"
                        )
                        email_validation = gr.HTML("", elem_id="email_validation")
                        
                        telefono = gr.Textbox(
                            label="Teléfono *",
                            placeholder="+34 666 123 456",
                            info="Con código de país",
                            lines=1,
                            elem_id="telefono_input"
                        )
                        phone_validation = gr.HTML("", elem_id="phone_validation")
                        
                        with gr.Row():
                            linkedin = gr.Textbox(
                                label="LinkedIn",
                                placeholder="linkedin.com/in/maria-garcia",
                                info="Tu perfil profesional",
                                lines=1,
                                elem_id="linkedin_input"
                            )
                            ubicacion = gr.Textbox(
                                label="Ubicación",
                                placeholder="Madrid, España",
                                info="Ciudad donde resides",
                                lines=1,
                                elem_id="ubicacion_input"
                            )
                        
                        linkedin_validation = gr.HTML("", elem_id="linkedin_validation")
                    
                    # Selector de plantilla CV
                    with gr.Group():
                        gr.Markdown("### 🎨 **Diseño de tu CV**")
                        
                        template_choices = [
                            ("🎨 Moderna - Diseño limpio y profesional", "modern"),
                            ("👔 Ejecutiva - Estilo tradicional para puestos senior", "executive"),  
                            ("🌈 Creativa - Para diseñadores y profesionales creativos", "creative"),
                            ("💻 Técnica - Optimizada para desarrolladores y IT", "technical")
                        ]
                        
                        template_selector = gr.Dropdown(
                            choices=template_choices,
                            value="modern",
                            label="Plantilla de CV",
                            info="🎯 Elige según tu sector profesional",
                            interactive=True
                        )
                        
                        # Vista previa compacta de plantillas
                        gr.HTML("""
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px;">
                            <div style="padding: 8px; border: 1px solid #e5e7eb; border-radius: 6px; text-align: center; font-size: 0.8rem;">
                                <strong style="color: #2563eb;">🎨 Moderna</strong>
                            </div>
                            <div style="padding: 8px; border: 1px solid #e5e7eb; border-radius: 6px; text-align: center; font-size: 0.8rem;">
                                <strong style="color: #374151;">👔 Ejecutiva</strong>
                            </div>
                            <div style="padding: 8px; border: 1px solid #e5e7eb; border-radius: 6px; text-align: center; font-size: 0.8rem;">
                                <strong style="color: #7c3aed;">🌈 Creativa</strong>
                            </div>
                            <div style="padding: 8px; border: 1px solid #e5e7eb; border-radius: 6px; text-align: center; font-size: 0.8rem;">
                                <strong style="color: #16a34a;">💻 Técnica</strong>
                            </div>
                        </div>
                        """)
                    
                    # Configuración de IA
                    with gr.Group():
                        gr.Markdown("### 🤖 **Configuración de IA**")
                        
                        # Crear opciones con información visual mejorada
                        provider_choices = []
                        for key, config in API_CONFIGS.items():
                            if config["free"] == True:
                                status = "🆓 GRATIS"
                            elif config["free"] == "Tier gratuito disponible":
                                status = "💰 FREEMIUM"
                            else:
                                status = "💳 DE PAGO"
                            provider_choices.append((f"{config['name']} - {status}", key))
                        
                        api_provider = gr.Dropdown(
                            choices=provider_choices,
                            value="mock",
                            label="Proveedor de IA",
                            info="💡 Groq es gratis y rápido",
                            interactive=True
                        )
                        
                        modelo_seleccionado = gr.Dropdown(
                            choices=list(API_CONFIGS["mock"]["models"].keys()),
                            value="mock-professional",
                            label="Modelo de IA",
                            info="Según tu perfil profesional",
                            interactive=True
                        )
                        
                        api_key = gr.Textbox(
                            label="API Key",
                            placeholder="No requerida para el modo simulado",
                            type="password",
                            visible=False,
                            info="🎭 Modo simulado activo",
                            lines=1
                        )
                
                # ===================================================================
                # COLUMNA 2: EXPERIENCIA PROFESIONAL + EDUCACIÓN (33%)
                # ===================================================================
                with gr.Column(scale=1, min_width=350):
                    gr.Markdown("## 💼 **Experiencia Profesional**")
                    
                    # Perfil profesional
                    with gr.Group():
                        gr.Markdown("### 🎯 **Objetivo Profesional**")
                        
                        objetivo = gr.Textbox(
                            label="Describe tu objetivo",
                            placeholder="Ej: Desarrollador Full Stack especializado en React y Node.js buscando liderar equipos de desarrollo en una startup tecnológica",
                            info="Esto mejora significativamente la optimización ATS",
                            lines=3
                        )
                        
                        experiencia_anos = gr.Dropdown(
                            choices=["Sin experiencia", "0-1 años", "2-3 años", "4-5 años", "6-10 años", "10+ años"],
                            label="Años de Experiencia",
                            info="Selecciona tu rango de experiencia",
                            value="2-3 años"
                        )
                    
                    # Experiencia laboral
                    with gr.Group():
                        gr.Markdown("### 💼 **Historial Laboral**")
                        
                        experiencia_laboral = gr.Textbox(
                            label="Experiencia Laboral",
                            placeholder="""• Desarrollador Senior - TechCorp (2020-2024)
  - Desarrollo de aplicaciones web con React y Node.js
  - Liderazgo de equipo de 3 desarrolladores
  - Implementación de metodologías ágiles

• Desarrollador Junior - StartupXYZ (2018-2020)
  - Desarrollo frontend con JavaScript y Vue.js
  - Colaboración en proyectos de e-commerce""",
                            info="Usa viñetas (•) para mejor formato. Incluye logros específicos.",
                            lines=8
                        )
                    
                    # Educación
                    with gr.Group():
                        gr.Markdown("### 🎓 **Formación Académica**")
                        
                        educacion = gr.Textbox(
                            label="Educación y Certificaciones",
                            placeholder="""• Grado en Ingeniería Informática - Universidad Complutense Madrid (2014-2018)
• Máster en Desarrollo Web - UNIR (2019-2020)
• Certificación AWS Solutions Architect (2023)
• Curso Advanced React - Platzi (2022)""",
                            info="Incluye títulos, certificaciones, cursos relevantes",
                            lines=6
                        )
                
                # ===================================================================
                # COLUMNA 3: HABILIDADES + EXTRAS + GENERACIÓN (33%)
                # ===================================================================
                with gr.Column(scale=1, min_width=320):
                    gr.Markdown("## 🎯 **Habilidades y Competencias**")
                    
                    # Habilidades técnicas
                    with gr.Group():
                        gr.Markdown("### 🛠️ **Habilidades Técnicas**")
                        
                        habilidades = gr.Textbox(
                            label="Habilidades y Competencias",
                            placeholder="""• Lenguajes: JavaScript, Python, Java, TypeScript
• Frontend: React, Vue.js, HTML5, CSS3, Sass
• Backend: Node.js, Express, Django, REST APIs
• Bases de datos: MongoDB, PostgreSQL, MySQL
• DevOps: Docker, AWS, Git, CI/CD
• Metodologías: Scrum, Agile, TDD""",
                            info="Organiza por categorías para mejor lectura",
                            lines=6
                        )
                    
                    # Idiomas
                    with gr.Group():
                        gr.Markdown("### 🌍 **Idiomas**")
                        
                        idiomas = gr.Textbox(
                            label="Idiomas",
                            placeholder="""• Español - Nativo
• Inglés - Avanzado (C1)
• Francés - Intermedio (B2)""",
                            info="Incluye el nivel según el Marco Común Europeo",
                            lines=3
                        )
                    
                    # Información adicional consolidada
                    with gr.Group():
                        gr.Markdown("### ✨ **Información Adicional**")
                        
                        with gr.Accordion("📋 Certificaciones", open=False):
                            certificaciones = gr.Textbox(
                                label="Certificaciones",
                                placeholder="• AWS Solutions Architect (2023)\n• Google Analytics Certified (2022)\n• Scrum Master Certified (2021)",
                                info="Certificaciones profesionales relevantes",
                                lines=3
                            )
                        
                        with gr.Accordion("🚀 Proyectos Destacados", open=False):
                            proyectos = gr.Textbox(
                                label="Proyectos",
                                placeholder="• E-commerce Platform - React + Node.js\n• Task Management App - Vue.js + Firebase\n• API RESTful - Python + Django",
                                info="Proyectos que demuestren tus habilidades",
                                lines=3
                            )
                    
                    # Zona de generación
                    gr.Markdown("---")
                    gr.Markdown("## 🚀 **Generar tu CV**")
                    
                    # Información de ATS
                    gr.HTML("""
                    <div style="background: linear-gradient(135deg, #fef3c7, #fde68a); padding: 12px; border-radius: 8px; margin-bottom: 16px; text-align: center;">
                        <div style="font-weight: 600; color: #92400e; font-size: 0.95rem;">🎯 Optimización ATS Automática</div>
                        <div style="font-size: 0.8rem; color: #a16207; margin-top: 2px;">Palabras clave añadidas según tu sector</div>
                    </div>
                    """)
                    
                    # Botones de acción
                    with gr.Row():
                        generar_btn = gr.Button(
                            "🤖 Generar CV",
                            variant="primary",
                            size="lg",
                            scale=1,
                            elem_id="generate_button"
                        )
                    
                    with gr.Row():
                        live_preview_toggle = gr.Button(
                            "👁️ Vista Previa en Vivo",
                            variant="secondary",
                            size="sm",
                            scale=1,
                            elem_id="live_preview_toggle"
                        )
                    
                    # Indicador de progreso
                    progress_html = gr.HTML(visible=False)
            
            # ===================================================================
            # ÁREA DE RESULTADOS (Ancho completo)
            # ===================================================================
            gr.Markdown("---")
            gr.Markdown("## 📄 **Resultado Generado**")
            
            with gr.Row():
                with gr.Column(scale=2):
                    resultado_texto = gr.Markdown()
                
                with gr.Column(scale=1):
                    archivo_descarga = gr.File(
                        label="📁 **Descargar CV (PDF)**",
                        visible=True,
                        height=120
                    )
            
            # ===================================================================
            # EVENT HANDLERS
            # ===================================================================
            
            # Conectar el botón con la función
            generar_btn.click(
                fn=self.generate_cv,
                inputs=[
                    nombre, email, telefono, linkedin, ubicacion, objetivo,
                    experiencia_anos, experiencia_laboral, educacion, 
                    habilidades, idiomas, template_selector, api_provider, modelo_seleccionado, api_key,
                    certificaciones, proyectos
                ],
                outputs=[resultado_texto, archivo_descarga]
            )
            
            # Event handlers para UI dinámica
            api_provider.change(
                fn=self.update_models_dropdown,
                inputs=[api_provider],
                outputs=[modelo_seleccionado]
            )
            
            api_provider.change(
                fn=self.update_api_key_visibility,
                inputs=[api_provider],
                outputs=[api_key]
            )
            
            # Validaciones en tiempo real
            email.change(
                fn=self.validate_email_realtime,
                inputs=[email],
                outputs=[email_validation]
            )
            
            telefono.change(
                fn=self.validate_phone_realtime,
                inputs=[telefono],
                outputs=[phone_validation]
            )
            
            linkedin.change(
                fn=self.validate_linkedin_realtime,
                inputs=[linkedin],
                outputs=[linkedin_validation]
            )
            
            # Live Preview Toggle Handler
            live_preview_state = gr.State(False)
            
            def toggle_live_preview(current_state):
                new_state = not current_state
                if new_state:
                    return new_state, "🔴 Desactivar Vista Previa"
                else:
                    return new_state, "👁️ Activar Vista Previa"
            
            live_preview_toggle.click(
                fn=toggle_live_preview,
                inputs=[live_preview_state],
                outputs=[live_preview_state, live_preview_toggle]
            )
            
            # Footer informativo
            gr.HTML("""
            <div style="text-align: center; padding: 2rem; color: #6b7280; border-top: 1px solid #e5e7eb; margin-top: 2rem;">
                <p>🚀 <strong>CV Creator AI</strong> - Potenciado por Inteligencia Artificial</p>
                <p style="font-size: 0.9rem;">✨ Genera CVs profesionales optimizados para ATS en segundos</p>
            </div>
            """)
        
        return demo
    
    def get_custom_css(self) -> str:
        """CSS personalizado mejorado con diseño responsivo"""
        return """
        /* Estilos globales */
        .gradio-container {
            max-width: 1400px !important;
            margin: 0 auto !important;
        }
        
        /* Animaciones suaves */
        .gr-button {
            transition: all 0.3s ease !important;
            border-radius: 8px !important;
        }
        
        .gr-button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        }
        
        /* Botón principal destacado */
        #generate_button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            border: none !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
        }
        
        #generate_button:hover {
            background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%) !important;
        }
        
        /* Campos de entrada mejorados */
        .gr-textbox, .gr-dropdown {
            border-radius: 8px !important;
            border: 2px solid #e5e7eb !important;
            transition: all 0.3s ease !important;
        }
        
        .gr-textbox:focus, .gr-dropdown:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }
        
        /* Grupos y secciones */
        .gr-group {
            border-radius: 12px !important;
            border: 1px solid #e5e7eb !important;
            padding: 16px !important;
            margin-bottom: 16px !important;
            background: #fafafa !important;
        }
        
        /* Validaciones */
        .validation-success {
            color: #10b981 !important;
            background: #ecfdf5 !important;
            padding: 4px 8px !important;
            border-radius: 4px !important;
            font-size: 0.85rem !important;
        }
        
        .validation-error {
            color: #ef4444 !important;
            background: #fef2f2 !important;
            padding: 4px 8px !important;
            border-radius: 4px !important;
            font-size: 0.85rem !important;
        }
        
        /* Responsivo */
        @media (max-width: 768px) {
            .gradio-container {
                padding: 0 16px !important;
            }
            
            .gr-row {
                flex-direction: column !important;
            }
            
            .gr-column {
                min-width: 100% !important;
                margin-bottom: 16px !important;
            }
        }
        
        /* Dark mode compatibility */
        .dark .gr-group {
            background: #1f2937 !important;
            border-color: #374151 !important;
        }
        """
    
    def generate_cv(self, nombre: str, email: str, telefono: str, linkedin: str, 
                   ubicacion: str, objetivo: str, experiencia_anos: str,
                   experiencia_laboral: str, educacion: str, habilidades: str,
                   idiomas: str, template: str, api_provider: str, 
                   modelo: str, api_key: str, certificaciones: str = "", proyectos: str = "") -> Tuple[str, Optional[str]]:
        """Generar CV con validaciones y manejo de errores mejorado"""
        
        try:
            # Validaciones básicas
            if not all([nombre.strip(), email.strip(), telefono.strip()]):
                return "❌ **Error:** Los campos Nombre, Email y Teléfono son obligatorios.", None
            
            # Validaciones de formato
            if not validate_email(email):
                return "❌ **Error:** El formato del email no es válido.", None
            
            if not validate_phone(telefono):
                return "❌ **Error:** El formato del teléfono no es válido.", None
            
            if linkedin and not validate_linkedin(linkedin):
                return "❌ **Error:** El formato del LinkedIn no es válido.", None
            
            # Configurar el servicio de IA
            self.ai_service.configure(api_provider, modelo, api_key)
            
            # Preparar datos del usuario
            user_data = {
                "nombre": clean_text(nombre),
                "email": clean_text(email),
                "telefono": clean_text(telefono),
                "linkedin": clean_text(linkedin) if linkedin else "",
                "ubicacion": clean_text(ubicacion) if ubicacion else "",
                "objetivo": clean_text(objetivo) if objetivo else "",
                "experiencia_anos": experiencia_anos,
                "experiencia_laboral": clean_text(experiencia_laboral) if experiencia_laboral else "",
                "educacion": clean_text(educacion) if educacion else "",
                "habilidades": clean_text(habilidades) if habilidades else "",
                "idiomas": clean_text(idiomas) if idiomas else "",
                "certificaciones": clean_text(certificaciones) if certificaciones else "",
                "proyectos": clean_text(proyectos) if proyectos else ""
            }
            
            # Generar contenido del CV
            logger.info(f"Generando CV para {nombre} con plantilla {template}")
            cv_content = self.content_generator.generate_cv_content(
                user_data, 
                template, 
                self.ai_service
            )
            
            # Generar PDF
            pdf_path = self.pdf_generator.generate_pdf(cv_content, template, user_data)
            
            # Autoguardar datos (opcional)
            if self.autosave_enabled:
                self.save_user_data(user_data)
            
            # Resultado en Markdown para mostrar
            preview_content = f"""
# ✅ **CV Generado Exitosamente**

## 📋 **Resumen del CV:**
- **Nombre:** {nombre}
- **Plantilla:** {template.title()}
- **Proveedor IA:** {api_provider}
- **Modelo:** {modelo}

## 📄 **Vista Previa del Contenido:**

{cv_content[:1000]}...

---
💡 **Tip:** Tu CV ha sido optimizado automáticamente para sistemas ATS con palabras clave relevantes para tu sector.
            """
            
            return preview_content, pdf_path
            
        except Exception as e:
            logger.error(f"Error generando CV: {str(e)}")
            error_message = f"""
❌ **Error generando el CV:**

```
{str(e)}
```

🔧 **Posibles soluciones:**
1. Verifica que todos los campos obligatorios estén completos
2. Si usas una API externa, verifica tu API key
3. Intenta con otra plantilla o modelo
4. Contacta al soporte si el problema persiste
            """
            return error_message, None
    
    def update_models_dropdown(self, provider: str) -> gr.Dropdown:
        """Actualizar modelos disponibles según el proveedor"""
        if provider in API_CONFIGS:
            models = list(API_CONFIGS[provider]["models"].keys())
            return gr.Dropdown(choices=models, value=models[0] if models else None)
        return gr.Dropdown(choices=[], value=None)
    
    def update_api_key_visibility(self, provider: str) -> gr.Textbox:
        """Mostrar/ocultar campo API key según el proveedor"""
        if provider == "mock":
            return gr.Textbox(visible=False, info="🎭 Modo simulado - no se requiere API key")
        else:
            config = API_CONFIGS.get(provider, {})
            return gr.Textbox(
                visible=True, 
                info=f"🔑 API key requerida para {config.get('name', provider)}"
            )
    
    def validate_email_realtime(self, email: str) -> str:
        """Validación de email en tiempo real"""
        if not email:
            return ""
        
        if validate_email(email):
            return '<div class="validation-success">✅ Email válido</div>'
        else:
            return '<div class="validation-error">❌ Formato de email inválido</div>'
    
    def validate_phone_realtime(self, phone: str) -> str:
        """Validación de teléfono en tiempo real"""
        if not phone:
            return ""
        
        if validate_phone(phone):
            return '<div class="validation-success">✅ Teléfono válido</div>'
        else:
            return '<div class="validation-error">❌ Formato: +34 666 123 456</div>'
    
    def validate_linkedin_realtime(self, linkedin: str) -> str:
        """Validación de LinkedIn en tiempo real"""
        if not linkedin:
            return ""
        
        if validate_linkedin(linkedin):
            return '<div class="validation-success">✅ LinkedIn válido</div>'
        else:
            return '<div class="validation-error">❌ Formato: linkedin.com/in/usuario</div>'
    
    def save_user_data(self, user_data: Dict[str, Any]) -> None:
        """Guardar datos del usuario para autocompletado futuro"""
        try:
            # Crear directorio de datos si no existe
            data_dir = "data"
            os.makedirs(data_dir, exist_ok=True)
            
            # Guardar datos (sin información sensible)
            safe_data = {k: v for k, v in user_data.items() if k not in ['email', 'telefono']}
            
            with open(os.path.join(data_dir, "last_user_data.json"), 'w', encoding='utf-8') as f:
                json.dump(safe_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.warning(f"No se pudo guardar datos del usuario: {e}")

if __name__ == "__main__":
    # Crear y lanzar la aplicación
    app = CVGeneratorApp()
    demo = app.create_interface()
    
    # Configuración de lanzamiento
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True,
        show_error=True,
        quiet=False,
        favicon_path=None,
        ssl_keyfile=None,
        ssl_certfile=None,
        ssl_keyfile_password=None
    )