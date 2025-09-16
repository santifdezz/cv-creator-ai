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
    
    def show_progress(self, message):
        """Muestra indicador de progreso"""
        return f"""
        <div class="progress-container" style="background: linear-gradient(135deg, #fef3c7, #fde68a); border: 1px solid #f59e0b; border-radius: 12px; padding: 1rem; text-align: center; margin: 1rem 0;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                <div style="width: 20px; height: 20px; border: 2px solid #f59e0b; border-top: 2px solid transparent; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                <strong style="color: #92400e;">{message}</strong>
            </div>
        </div>
        """
        
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
        """Crea la interfaz de Gradio con diseño mejorado y optimización móvil"""
        
        # CSS mejorado para mejor UX y mobile-first design
        enhanced_css = """
        /* Variables CSS para consistencia */
        :root {
            --primary-color: #2563eb;
            --primary-dark: #1d4ed8;
            --secondary-color: #f8fafc;
            --accent-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --text-primary: #1f2937;
            --text-secondary: #6b7280;
            --border-color: #e5e7eb;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            --border-radius: 12px;
        }
        
        /* Contenedor principal optimizado */
        .gradio-container {
            max-width: 1400px !important;
            margin: 0 auto !important;
            padding: 20px !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }
        
        /* Header mejorado */
        .main-header {
            text-align: center;
            background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
            color: white;
            padding: 2rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            box-shadow: var(--shadow-md);
        }
        
        .main-header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .main-header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        /* Botones principales mejorados */
        .gr-button-primary {
            background: linear-gradient(135deg, var(--primary-color), var(--primary-dark)) !important;
            border: none !important;
            border-radius: var(--border-radius) !important;
            padding: 16px 32px !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: var(--shadow-md) !important;
            text-transform: none !important;
        }
        
        .gr-button-primary:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3) !important;
        }
        
        .gr-button-secondary {
            background: white !important;
            border: 2px solid var(--primary-color) !important;
            color: var(--primary-color) !important;
            border-radius: var(--border-radius) !important;
            padding: 12px 24px !important;
            font-weight: 500 !important;
        }
        
        /* Cards y secciones */
        .gr-form, .gr-panel {
            background: white !important;
            border: 1px solid var(--border-color) !important;
            border-radius: var(--border-radius) !important;
            padding: 24px !important;
            margin-bottom: 20px !important;
            box-shadow: var(--shadow-sm) !important;
            transition: box-shadow 0.3s ease !important;
        }
        
        .gr-form:hover, .gr-panel:hover {
            box-shadow: var(--shadow-md) !important;
        }
        
        /* Campos de entrada mejorados */
        .gr-textbox, .gr-dropdown, .gr-textarea {
            border: 2px solid var(--border-color) !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
        }
        
        .gr-textbox:focus, .gr-dropdown:focus, .gr-textarea:focus {
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
            outline: none !important;
        }
        
        /* Labels mejorados */
        .gr-label {
            font-weight: 600 !important;
            color: var(--text-primary) !important;
            margin-bottom: 8px !important;
            font-size: 0.95rem !important;
        }
        
        /* Status indicators */
        .status-success {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            padding: 16px;
            border-radius: var(--border-radius);
            margin: 16px 0;
        }
        
        .status-error {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
            padding: 16px;
            border-radius: var(--border-radius);
            margin: 16px 0;
        }
        
        /* Responsive design - Mobile First */
        @media (max-width: 768px) {
            .gradio-container {
                padding: 12px !important;
            }
            
            .main-header h1 {
                font-size: 2rem;
            }
            
            .gr-form, .gr-panel {
                padding: 16px !important;
                margin-bottom: 16px !important;
            }
            
            .gr-button-primary {
                width: 100% !important;
                padding: 16px !important;
                font-size: 1rem !important;
            }
            
            .gr-textbox, .gr-dropdown, .gr-textarea {
                padding: 14px !important;
                font-size: 16px !important; /* Evita zoom en iOS */
            }
        }
        
        /* Mejoras para tablets */
        @media (min-width: 769px) and (max-width: 1024px) {
            .gradio-container {
                padding: 16px !important;
            }
        }
        
        /* Accordion mejorado */
        .gr-accordion {
            border: 1px solid var(--border-color) !important;
            border-radius: var(--border-radius) !important;
            overflow: hidden !important;
        }
        
        /* Loading states */
        .gr-loading {
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
        }
        
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        /* File upload mejorado */
        .gr-file {
            border: 2px dashed var(--border-color) !important;
            border-radius: var(--border-radius) !important;
            padding: 24px !important;
            text-align: center !important;
            transition: all 0.3s ease !important;
        }
        
        .gr-file:hover {
            border-color: var(--primary-color) !important;
            background: rgba(37, 99, 235, 0.05) !important;
        }
        
        /* Progress bar mejorado */
        .progress-bar {
            width: 100%;
            height: 8px;
            background: var(--border-color);
            border-radius: 4px;
            overflow: hidden;
            margin: 16px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
            border-radius: 4px;
            transition: width 0.3s ease;
        }
        
        /* Tooltips */
        .tooltip {
            position: relative;
            display: inline-block;
        }
        
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 200px;
            background-color: var(--text-primary);
            color: white;
            text-align: center;
            border-radius: 6px;
            padding: 8px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            font-size: 0.85rem;
        }
        
        .tooltip:hover .tooltiptext {
            visibility: visible;
        }
        
        /* Animation for progress indicator */
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        """
        
        with gr.Blocks(
            title="🤖 Generador Automático de CV con IA",
            theme=gr.themes.Soft(
                primary_hue="blue",
                secondary_hue="gray",
                neutral_hue="slate",
                font=gr.themes.GoogleFont("Inter")
            ),
            css=enhanced_css,
            analytics_enabled=False
        ) as iface:
            
            # Header mejorado con estadísticas
            with gr.Row():
                gr.HTML("""
                <div class="main-header">
                    <h1>🤖 Generador Automático de CV con IA</h1>
                    <p>Crea tu currículum profesional optimizado para ATS en minutos</p>
                    <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem; flex-wrap: wrap;">
                        <div style="text-align: center;">
                            <div style="font-size: 1.5rem; font-weight: bold;">8+</div>
                            <div style="font-size: 0.9rem; opacity: 0.8;">Proveedores IA</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 1.5rem; font-weight: bold;">100%</div>
                            <div style="font-size: 0.9rem; opacity: 0.8;">Compatible ATS</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 1.5rem; font-weight: bold;">30s</div>
                            <div style="font-size: 0.9rem; opacity: 0.8;">Tiempo promedio</div>
                        </div>
                    </div>
                </div>
                """)
            
            # Contenido principal con mejor organización
            with gr.Row(equal_height=False):
                # Columna izquierda: Configuración IA (30%)
                with gr.Column(scale=3, min_width=300):
                    gr.Markdown("## 🤖 Configuración de IA")
                    
                    with gr.Group():
                        gr.Markdown("### 🎯 Selecciona tu Proveedor")
                        
                        # Crear opciones con información visual mejorada
                        provider_choices = []
                        for key, config in API_CONFIGS.items():
                            if config["free"] == True:
                                status = "🆓 GRATIS"
                                color = "#10b981"
                            elif config["free"] == "Tier gratuito disponible":
                                status = "💰 FREEMIUM"
                                color = "#f59e0b"
                            else:
                                status = "💳 DE PAGO"
                                color = "#ef4444"
                            provider_choices.append((f"{config['name']} - {status}", key))
                        
                        api_provider = gr.Dropdown(
                            choices=provider_choices,
                            value="mock",
                            label="Proveedor de IA",
                            info="💡 Recomendamos empezar con Groq (gratis y rápido)",
                            interactive=True
                        )
                        
                        modelo_seleccionado = gr.Dropdown(
                            choices=list(API_CONFIGS["mock"]["models"].keys()),
                            value="mock-professional",
                            label="Modelo de IA",
                            info="Elige el modelo que mejor se adapte a tu perfil",
                            interactive=True
                        )
                        
                        api_key = gr.Textbox(
                            label="API Key",
                            placeholder="No requerida para el modo simulado",
                            type="password",
                            visible=False,
                            info="🎭 Modo simulado - no se requiere API key",
                            lines=1
                        )
                    
                    # Información de APIs mejorada
                    with gr.Accordion("💡 Guía de Proveedores", open=False):
                        gr.HTML("""
                        <div style="padding: 16px; background: linear-gradient(135deg, #f0f9ff, #e0f2fe); border-radius: 12px;">
                            <h4 style="color: #0369a1; margin-top: 0;">🆓 Opciones Gratuitas</h4>
                            <ul style="margin: 8px 0; padding-left: 20px;">
                                <li><strong>🎭 Simulado:</strong> Sin API, usa plantillas optimizadas ATS</li>
                                <li><strong>⚡ Groq:</strong> Súper rápido y gratuito (recomendado)</li>
                                <li><strong>🏠 Ollama:</strong> Instala modelos en tu PC (ilimitado)</li>
                            </ul>
                            
                            <h4 style="color: #059669; margin: 16px 0 8px 0;">💳 Opciones Premium</h4>
                            <ul style="margin: 8px 0; padding-left: 20px;">
                                <li><strong>🤖 OpenAI:</strong> GPT-4 máxima calidad (~$0.03/CV)</li>
                                <li><strong>🧠 Claude:</strong> Excelente escritura (~$0.01/CV)</li>
                            </ul>
                            
                            <div style="background: #fef3c7; padding: 12px; border-radius: 8px; margin-top: 16px;">
                                <strong>💡 Consejo:</strong> Empieza con <strong>Groq</strong> para pruebas gratuitas
                            </div>
                        </div>
                        """)
                
                # Columna central: Formulario principal (50%)
                with gr.Column(scale=5, min_width=400):
                    gr.Markdown("## 📝 Tu Información Profesional")
                    
                    # Información básica
                    with gr.Group():
                        gr.Markdown("### � **Datos Básicos** *(Obligatorio)*")
                        
                        nombre = gr.Textbox(
                            label="Nombre Completo *",
                            placeholder="Ej: María García López",
                            info="Tu nombre completo como aparecerá en el CV",
                            lines=1
                        )
                        
                        with gr.Row():
                            email = gr.Textbox(
                                label="Email *",
                                placeholder="maria.garcia@email.com",
                                info="Email profesional preferiblemente",
                                lines=1
                            )
                            telefono = gr.Textbox(
                                label="Teléfono *",
                                placeholder="+34 666 123 456",
                                info="Con código de país",
                                lines=1
                            )
                        
                        with gr.Row():
                            linkedin = gr.Textbox(
                                label="LinkedIn (Opcional)",
                                placeholder="linkedin.com/in/maria-garcia",
                                info="Solo el nombre de usuario o URL completa",
                                lines=1
                            )
                            ubicacion = gr.Textbox(
                                label="Ubicación (Opcional)",
                                placeholder="Madrid, España",
                                info="Ciudad y país donde resides",
                                lines=1
                            )
                    
                    # Perfil profesional
                    with gr.Group():
                        gr.Markdown("### 🎯 **Perfil Profesional**")
                        
                        objetivo = gr.Textbox(
                            label="Objetivo Profesional (Opcional)",
                            placeholder="Ej: Desarrollador Full Stack especializado en React y Node.js buscando liderar equipos de desarrollo en una startup tecnológica",
                            info="Describe tu objetivo o área de especialización (mejora significativamente el resultado)",
                            lines=3
                        )
                        
                        experiencia_anos = gr.Dropdown(
                            choices=["Sin experiencia", "0-1 años", "2-3 años", "4-5 años", "6-10 años", "10+ años"],
                            label="Años de Experiencia (Opcional)",
                            info="Selecciona tu rango de experiencia profesional",
                            value="2-3 años"
                        )
                    
                    # Experiencia y educación
                    with gr.Group():
                        gr.Markdown("### 💼 **Experiencia y Formación**")
                        
                        experiencia_laboral = gr.Textbox(
                            label="Experiencia Laboral (Opcional)",
                            placeholder="""Desarrollador Senior - TechCorp - 2020-2024
Desarrollador Junior - StartupXYZ - 2018-2020
Becario de Desarrollo - InnovaLab - 2017-2018""",
                            info="Una línea por trabajo: Puesto - Empresa - Período. Cuanta más información, mejor optimización ATS",
                            lines=6
                        )
                        
                        educacion = gr.Textbox(
                            label="Educación (Opcional)",
                            placeholder="""Grado en Ingeniería Informática - Universidad Complutense - 2018
Máster en Desarrollo Web - CEU San Pablo - 2019
Certificación AWS Solutions Architect - 2022""",
                            info="Una línea por titulación/certificación",
                            lines=4
                        )
                
                # Columna derecha: Habilidades y acción (30%)
                with gr.Column(scale=3, min_width=300):
                    gr.Markdown("## 🔧 Habilidades y Competencias")
                    
                    with gr.Group():
                        habilidades = gr.Textbox(
                            label="Habilidades Técnicas (Opcional)",
                            placeholder="JavaScript, React, Node.js, Python, SQL, Git, Docker, AWS, Agile, Scrum",
                            info="⚡ La IA las categorizará automáticamente y añadirá keywords ATS relevantes",
                            lines=5
                        )
                        
                        idiomas = gr.Textbox(
                            label="Idiomas (Opcional)",
                            placeholder="""Español - Nativo
Inglés - Avanzado (C1)
Francés - Intermedio (B2)""",
                            info="Una línea por idioma con nivel",
                            lines=4
                        )
                    
                    # Botón de generación destacado
                    gr.Markdown("### 🚀 **Generar tu CV**")
                    
                    with gr.Group():
                        gr.HTML("""
                        <div style="background: linear-gradient(135deg, #fef3c7, #fde68a); padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                            <div style="text-align: center;">
                                <div style="font-size: 1.1rem; font-weight: 600; color: #92400e;">🎯 Optimización ATS Automática</div>
                                <div style="font-size: 0.9rem; color: #a16207; margin-top: 4px;">Palabras clave técnicas añadidas automáticamente según tu sector</div>
                            </div>
                        </div>
                        """)
                        
                        generar_btn = gr.Button(
                            "🤖 Generar CV Profesional",
                            variant="primary",
                            size="lg",
                            scale=1
                        )
                        
                        # Indicador de progreso
                        progress_html = gr.HTML(visible=False)
            
            # Área de resultados mejorada
            gr.Markdown("---")
            gr.Markdown("## 📄 **Resultado Generado**")
            
            with gr.Row():
                with gr.Column(scale=2):
                    resultado_texto = gr.Markdown()
                
                with gr.Column(scale=1):
                    archivo_descarga = gr.File(
                        label="� **Descargar CV (PDF)**",
                        visible=True,
                        height=120
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