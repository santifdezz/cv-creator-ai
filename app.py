#!/usr/bin/env python3
"""
Generador Automático de CV con IA
Aplicación principal usando Gradio

Autor: Tu nombre
Fecha: 2025
"""

import gradio as gr
from src.config import API_CONFIGS
from src.ai_service import AIService
from src.pdf_generator import PDFGenerator
from src.utils import validate_form_data, format_success_message
import asyncio
import os

class CVGeneratorApp:
    def __init__(self):
        self.ai_service = AIService()
        self.pdf_generator = PDFGenerator()
        
    async def generate_cv(self, nombre, email, telefono, linkedin, ubicacion, objetivo, 
                         experiencia_anos, experiencia_laboral, educacion, 
                         habilidades, idiomas, api_provider, modelo_seleccionado, api_key):
        """Función principal para generar CV"""
        
        # Validar campos obligatorios
        validation_error = validate_form_data(nombre, email, telefono, api_provider, api_key)
        if validation_error:
            return validation_error, None
        
        # Crear diccionario con los datos del formulario
        form_data = {
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'linkedin': linkedin,
            'ubicacion': ubicacion,
            'objetivo': objetivo,
            'experiencia_anos': experiencia_anos,
            'experiencia_laboral': experiencia_laboral,
            'educacion': educacion,
            'habilidades': habilidades,
            'idiomas': idiomas
        }
        
        try:
            # Generar contenido con IA
            ai_content = await self.ai_service.generate_cv_content(
                form_data, 
                api_provider, 
                modelo_seleccionado, 
                api_key.strip() if api_key else None
            )
            
            # Crear PDF
            pdf_path = self.pdf_generator.create_cv_pdf(form_data, ai_content)
            
            # Formatear mensaje de éxito
            mensaje = format_success_message(nombre, api_provider, modelo_seleccionado, ai_content)
            
            return mensaje, pdf_path
            
        except Exception as e:
            return f"❌ Error al generar el CV: {str(e)}", None

    def update_models_dropdown(self, api_provider):
        """Actualiza el dropdown de modelos basado en el proveedor seleccionado"""
        if api_provider in API_CONFIGS:
            models = list(API_CONFIGS[api_provider]["models"].keys())
            return gr.Dropdown(choices=models, value=models[0] if models else None, visible=True)
        return gr.Dropdown(choices=[], visible=False)

    def update_api_key_visibility(self, api_provider):
        """Muestra u oculta el campo de API key basado en el proveedor"""
        config = API_CONFIGS.get(api_provider, {})
        requires_key = config.get("requires_key", False)
        is_free = config.get("free", False)
        
        if not requires_key:
            return gr.Textbox(visible=False)
        elif is_free == True:
            return gr.Textbox(
                visible=True, 
                placeholder="Ingresa tu API key gratuita",
                info="🆓 Proveedor gratuito - obtén tu key en su sitio web"
            )
        elif is_free == "Tier gratuito disponible":
            return gr.Textbox(
                visible=True, 
                placeholder="Ingresa tu API key",
                info="💰 Freemium - tier gratuito disponible"
            )
        else:
            return gr.Textbox(
                visible=True, 
                placeholder="Ingresa tu API key (de pago)",
                info="💳 Servicio de pago - se requiere API key válida"
            )

    def create_interface(self):
        """Crea la interfaz de Gradio"""
        
        with gr.Blocks(
            title="Generador Automático de CV con IA",
            theme=gr.themes.Soft(),
            css="""
            .gradio-container {max-width: 1200px !important}
            .gr-button-primary {background: linear-gradient(45deg, #1e3a8a, #3b82f6) !important}
            .gr-form {background: #f8fafc !important; padding: 20px !important; border-radius: 10px !important}
            """
        ) as iface:
            
            # Header
            gr.Markdown("""
            # 🤖 Generador Automático de CV con IA
            
            ### Crea tu currículum profesional en minutos con múltiples opciones de IA
            
            Utiliza diferentes proveedores de inteligencia artificial para generar un CV optimizado, profesional y compatible con sistemas ATS.
            
            ---
            """)
            
            with gr.Row():
                # Configuración de IA
                with gr.Column(scale=1):
                    gr.Markdown("## 🤖 Configuración de IA")
                    
                    with gr.Group():
                        gr.Markdown("### Selecciona el Proveedor de IA:")
                        
                        # Crear opciones con información sobre costos
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
                            info="Selecciona el servicio de IA a usar"
                        )
                        
                        modelo_seleccionado = gr.Dropdown(
                            choices=list(API_CONFIGS["mock"]["models"].keys()),
                            value="mock-model",
                            label="Modelo de IA",
                            info="Modelo específico a utilizar"
                        )
                        
                        api_key = gr.Textbox(
                            label="API Key",
                            placeholder="No requerida para el modo simulado",
                            type="password",
                            visible=False,
                            info="🎭 Modo simulado - no se requiere API key"
                        )
                        
                        # Eventos para actualizar UI dinámicamente
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
                    
                    # Información de APIs
                    with gr.Accordion("ℹ️ Guía de Proveedores de IA", open=False):
                        gr.Markdown("""
                        **🆓 OPCIONES GRATUITAS:**
                        - **🎭 Simulado**: Sin API, usa plantillas optimizadas
                        - **🏠 Ollama Local**: Instala Ollama en tu PC (totalmente gratis)
                        - **🤗 Hugging Face**: API gratuita con límites (requiere registro)
                        
                        **💰 OPCIONES FREEMIUM:**
                        - **🚀 Cohere**: Tier gratuito disponible
                        
                        **💳 OPCIONES DE PAGO:**
                        - **🤖 OpenAI**: GPT-3.5/4 (mejor calidad, costo por uso)
                        - **🧠 Anthropic**: Claude (excelente calidad, costo por uso)
                        
                        **🎯 Recomendaciones:**
                        - Para **pruebas**: Usa modo "Simulado"
                        - Para **uso gratuito**: Ollama Local o Hugging Face
                        - Para **mejor calidad**: OpenAI o Anthropic (de pago)
                        """)
                
                # Formulario de datos personales
                with gr.Column(scale=2):
                    gr.Markdown("## 📝 Información Personal *(Obligatorio)*")
                    
                    with gr.Group():
                        nombre = gr.Textbox(
                            label="Nombre Completo *",
                            placeholder="Juan Pérez García",
                            info="Tu nombre completo como aparecerá en el CV"
                        )
                        
                        with gr.Row():
                            email = gr.Textbox(
                                label="Email *",
                                placeholder="juan.perez@email.com",
                                info="Tu dirección de correo profesional"
                            )
                            telefono = gr.Textbox(
                                label="Teléfono *",
                                placeholder="+34 666 123 456",
                                info="Número de contacto"
                            )
                        
                        with gr.Row():
                            linkedin = gr.Textbox(
                                label="LinkedIn (Opcional)",
                                placeholder="linkedin.com/in/juanperez",
                                info="Tu perfil de LinkedIn"
                            )
                            ubicacion = gr.Textbox(
                                label="Ubicación (Opcional)",
                                placeholder="Madrid, España",
                                info="Ciudad y país"
                            )
                    
                    gr.Markdown("## 🎯 Perfil Profesional")
                    
                    with gr.Group():
                        objetivo = gr.Textbox(
                            label="Objetivo Profesional (Opcional)",
                            placeholder="Desarrollador Full Stack especializado en React y Node.js",
                            info="Describe brevemente tu enfoque profesional",
                            lines=2
                        )
                        
                        experiencia_anos = gr.Dropdown(
                            choices=["0-1 años", "2-3 años", "4-5 años", "6-10 años", "10+ años"],
                            label="Años de Experiencia (Opcional)",
                            info="Selecciona tu rango de experiencia"
                        )
                    
                    gr.Markdown("## 💼 Experiencia y Formación")
                    
                    with gr.Group():
                        experiencia_laboral = gr.Textbox(
                            label="Experiencia Laboral (Opcional)",
                            placeholder="""Desarrollador Senior - TechCorp - 2020-2024
Desarrollador Junior - StartupXYZ - 2018-2020""",
                            info="Una línea por trabajo: Puesto - Empresa - Período",
                            lines=5
                        )
                        
                        educacion = gr.Textbox(
                            label="Educación (Opcional)",
                            placeholder="""Grado en Ingeniería Informática - Universidad Complutense - 2018
Máster en Desarrollo Web - CEU - 2019""",
                            info="Una línea por titulación",
                            lines=3
                        )
                
                # Habilidades y botón de generación
                with gr.Column(scale=1):
                    gr.Markdown("## 🔧 Habilidades")
                    
                    with gr.Group():
                        habilidades = gr.Textbox(
                            label="Habilidades (Opcional)",
                            placeholder="JavaScript, React, Node.js, Python, SQL, Git, Liderazgo, Trabajo en equipo",
                            info="Separadas por comas. La IA las categorizará automáticamente",
                            lines=4
                        )
                        
                        idiomas = gr.Textbox(
                            label="Idiomas (Opcional)",
                            placeholder="""Español - Nativo
Inglés - Avanzado (C1)
Francés - Intermedio (B2)""",
                            info="Una línea por idioma con nivel",
                            lines=3
                        )
                    
                    gr.Markdown("## 🚀 Generar CV")
                    
                    generar_btn = gr.Button(
                        "🤖 Generar CV con IA",
                        variant="primary",
                        size="lg"
                    )
            
            # Área de resultados
            gr.Markdown("---")
            
            with gr.Row():
                resultado_texto = gr.Markdown()
                
            with gr.Row():
                archivo_descarga = gr.File(
                    label="📄 Descargar CV (PDF)",
                    visible=True
                )
            
            # Conectar el botón con la función
            generar_btn.click(
                fn=self.generate_cv,
                inputs=[
                    nombre, email, telefono, linkedin, ubicacion, objetivo,
                    experiencia_anos, experiencia_laboral, educacion, 
                    habilidades, idiomas, api_provider, modelo_seleccionado, api_key
                ],
                outputs=[resultado_texto, archivo_descarga]
            )
            
            # Información adicional
            with gr.Accordion("📋 Consejos para un CV exitoso", open=False):
                gr.Markdown("""
                ### ✅ Mejores Prácticas:
                
                - **Sé específico**: Incluye logros cuantificables cuando sea posible
                - **Palabras clave**: Usa términos relevantes a tu industria para optimización ATS  
                - **Brevedad**: Mantén descripciones concisas pero impactantes
                - **Actualización**: Revisa y actualiza regularmente tu información
                
                ### 🎨 Características del CV generado:
                
                - ✅ **Compatible con ATS** (Applicant Tracking Systems)
                - ✅ **Diseño profesional y moderno** 
                - ✅ **Formato estándar** reconocido por recruiters
                - ✅ **Optimización con IA** para mejorar el contenido
                - ✅ **Estructura clara** y fácil de leer
                """)
            
            gr.Markdown("""
            ---
            <div style='text-align: center; color: #6b7280; font-size: 14px;'>
                💡 <strong>Tip:</strong> Después de generar tu CV, revísalo y personalízalo según la oferta de trabajo específica.<br>
                🔗 <strong>GitHub:</strong> <a href="https://github.com/santifdezz/cv-creator-ai" target="_blank">cv-creator-ai</a> | 
                ⭐ Si te ha sido útil, ¡dale una estrella al repo!
            </div>
            """)
        
        return iface

def main():
    """Función principal"""
    # Verificar dependencias
    try:
        import reportlab
        print("✅ ReportLab encontrado")
    except ImportError:
        print("⚠️ Instalando ReportLab...")
        os.system("pip install reportlab")
        import reportlab
    
    # Crear aplicación
    app = CVGeneratorApp()
    interface = app.create_interface()
    
    # Configuración de lanzamiento
    interface.launch(
        share=True,  # Generar enlace público
        server_name="0.0.0.0",  # Permitir acceso desde cualquier IP
        server_port=7860,  # Puerto estándar de Hugging Face Spaces
        show_error=True,  # Mostrar errores en la interfaz
        debug=False  # Modo debug para desarrollo
    )

if __name__ == "__main__":
    main()