#!/usr/bin/env python3
"""
Generador Automático de CV con IA - Versión Hugging Face Spaces
Aplicación principal usando Gradio

Autor: Tu nombre
Fecha: 2025
"""

import gradio as gr
import os
import sys

# Añadir el directorio src al path para las importaciones
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from config import API_CONFIGS
    from ai_service import AIService
    from pdf_generator import PDFGenerator
    from utils import validate_form_data, format_success_message
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all modules are in the src directory")
    sys.exit(1)

import asyncio


def create_interface():
    """Crear la interfaz principal de Gradio"""
    
    # Inicializar servicios
    ai_service = AIService()
    pdf_generator = PDFGenerator()
    
    # Función principal para generar CV
    def generate_cv(template, nombre, apellidos, email, telefono, linkedin, 
                   resumen_profesional, experiencia, formacion, habilidades, 
                   idiomas, certificaciones, proyectos, referencias, 
                   extra_fields):
        """Generar CV con IA y crear PDF"""
        try:
            # Validar datos del formulario
            form_data = {
                'nombre': nombre,
                'apellidos': apellidos,
                'email': email,
                'telefono': telefono,
                'linkedin': linkedin,
                'resumen_profesional': resumen_profesional,
                'experiencia': experiencia,
                'formacion': formacion,
                'habilidades': habilidades,
                'idiomas': idiomas,
                'certificaciones': certificaciones,
                'proyectos': proyectos,
                'referencias': referencias,
                'extra_fields': extra_fields
            }
            
            is_valid, validation_errors = validate_form_data(form_data)
            if not is_valid:
                return None, f"❌ **Errores de validación:**\n" + "\n".join([f"• {error}" for error in validation_errors])
            
            # Generar contenido con IA (si está configurado)
            enhanced_data = form_data.copy()
            if ai_service and hasattr(ai_service, 'enhance_cv_content'):
                try:
                    enhanced_data = ai_service.enhance_cv_content(form_data)
                except Exception as e:
                    print(f"Error enhancing content with AI: {e}")
                    # Continuar con los datos originales si falla la IA
            
            # Generar PDF
            pdf_path = pdf_generator.create_cv_pdf(enhanced_data, template=template)
            
            if pdf_path and os.path.exists(pdf_path):
                success_message = format_success_message(enhanced_data, template)
                return pdf_path, success_message
            else:
                return None, "❌ **Error:** No se pudo generar el archivo PDF"
                
        except Exception as e:
            return None, f"❌ **Error inesperado:** {str(e)}"
    
    # Funciones de validación en tiempo real
    def validate_email_realtime(email):
        if not email:
            return ""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return "✅ Email válido"
        else:
            return "❌ Formato de email inválido"
    
    def validate_phone_realtime(phone):
        if not phone:
            return ""
        import re
        # Acepta formatos: +34 123 456 789, 123-456-789, 123456789
        pattern = r'^(\+\d{1,3}[-.\s]?)?\d{3}[-.\s]?\d{3}[-.\s]?\d{3}$'
        if re.match(pattern, phone.replace(" ", "")):
            return "✅ Teléfono válido"
        else:
            return "❌ Formato de teléfono inválido"
    
    def validate_linkedin_realtime(linkedin):
        if not linkedin:
            return ""
        import re
        pattern = r'^(https?://)?(www\.)?linkedin\.com/(in|pub)/[a-zA-Z0-9-]+/?$'
        if re.match(pattern, linkedin):
            return "✅ LinkedIn válido"
        else:
            return "❌ Formato de LinkedIn inválido (ej: linkedin.com/in/tu-perfil)"

    # CSS personalizado
    custom_css = """
    <style>
        /* Variables CSS */
        :root {
            --primary-color: #2563eb;
            --secondary-color: #64748b;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --background-color: #f8fafc;
            --surface-color: #ffffff;
            --border-color: #e2e8f0;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --border-radius: 8px;
        }
        
        /* Reset y base */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* Contenedor principal */
        .gradio-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
            padding: 2rem !important;
            background: var(--background-color) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }
        
        /* Header principal */
        .main-header {
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, var(--primary-color), #3b82f6);
            color: white;
            border-radius: var(--border-radius);
            margin-bottom: 3rem;
            box-shadow: var(--shadow-md);
        }
        
        .main-header h1 {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            letter-spacing: -0.025em;
        }
        
        .main-header p {
            font-size: 1.125rem;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.7;
        }
        
        /* Template selector */
        .template-selector {
            background: var(--surface-color);
            padding: 2rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--border-color);
        }
        
        /* Grupos y paneles */
        .group,
        .panel {
            background: var(--surface-color) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: var(--border-radius) !important;
            padding: 2rem !important;
            margin-bottom: 2rem !important;
            box-shadow: var(--shadow-sm) !important;
            transition: all 0.3s ease !important;
        }
        
        .group:hover,
        .panel:hover {
            box-shadow: var(--shadow-md) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Botones */
        .gr-button {
            background: var(--primary-color) !important;
            color: white !important;
            border: none !important;
            border-radius: var(--border-radius) !important;
            padding: 1rem 2rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        .gr-button:hover {
            background: #1d4ed8 !important;
            transform: translateY(-1px) !important;
            box-shadow: var(--shadow-md) !important;
        }
        
        .gr-button:active {
            transform: translateY(0) !important;
        }
        
        /* Campos de entrada */
        .gr-textbox,
        .gr-dropdown,
        .gr-textarea {
            border: 1px solid var(--border-color) !important;
            border-radius: var(--border-radius) !important;
            padding: 1rem !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            background: var(--surface-color) !important;
        }
        
        .gr-textbox:focus,
        .gr-dropdown:focus,
        .gr-textarea:focus {
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
            outline: none !important;
        }
        
        /* Estado de éxito */
        .success-message {
            background: linear-gradient(135deg, var(--success-color), #059669);
            color: white;
            padding: 16px;
            border-radius: var(--border-radius);
            margin: 16px 0;
        }
        
        /* Estado de error */
        .error-message {
            background: linear-gradient(135deg, var(--error-color), #dc2626);
            color: white;
            padding: 16px;
            border-radius: var(--border-radius);
            margin: 16px 0;
        }
        
        /* Responsive design - Enhanced Mobile First */
        @media (max-width: 768px) {
            .gradio-container {
                padding: 0.5rem !important;
            }
            
            .main-header {
                padding: 1.5rem 1rem !important;
                margin-bottom: 1.5rem !important;
            }
            
            .main-header h1 {
                font-size: 1.8rem !important;
            }
            
            .group,
            .panel,
            .gr-form,
            .gr-panel {
                padding: 1rem !important;
                margin-bottom: 1rem !important;
            }
            
            .gr-row {
                flex-direction: column !important;
                gap: 1rem !important;
            }
            
            .gr-column {
                min-width: auto !important;
                width: 100% !important;
                margin-bottom: 1rem !important;
            }
            
            /* Touch-friendly buttons */
            .gr-button,
            .gr-button-primary {
                padding: 1rem 1.5rem !important;
                font-size: 1.1rem !important;
                width: 100% !important;
                min-height: 48px !important;
                touch-action: manipulation !important;
            }
            
            /* Mobile-optimized inputs */
            .gr-textbox,
            .gr-dropdown,
            .gr-textarea {
                font-size: 16px !important; /* Prevents zoom on iOS */
                padding: 1rem !important;
                min-height: 48px !important;
                touch-action: manipulation !important;
            }
        }
        
        /* Touch device optimizations */
        @media (hover: none) and (pointer: coarse) {
            .gr-button,
            .gr-textbox,
            .gr-dropdown,
            button,
            input,
            select {
                min-height: 44px !important;
                min-width: 44px !important;
            }
            
            body {
                -webkit-overflow-scrolling: touch;
                overflow-scrolling: touch;
            }
        }
    </style>
    """
    
    # JavaScript mejorado
    custom_js = """
    <script>
        // Auto-save functionality
        let autoSaveInterval;
        let lastSaveTime = Date.now();
        const SAVE_INTERVAL = 30000; // 30 seconds
        
        function initializeAutoSave() {
            console.log('🔄 Inicializando auto-guardado...');
            
            // Load saved data
            loadSavedData();
            
            // Set up auto-save interval
            autoSaveInterval = setInterval(saveFormData, SAVE_INTERVAL);
            
            // Save on form changes
            document.addEventListener('input', function(e) {
                if (e.target.matches('input, textarea, select')) {
                    // Debounce save
                    clearTimeout(window.saveTimeout);
                    window.saveTimeout = setTimeout(saveFormData, 2000);
                }
            });
            
            // Save before page unload
            window.addEventListener('beforeunload', saveFormData);
        }
        
        function saveFormData() {
            try {
                const formData = {};
                const inputs = document.querySelectorAll('input, textarea, select');
                
                inputs.forEach(input => {
                    if (input.id || input.name) {
                        const key = input.id || input.name;
                        formData[key] = input.value;
                    }
                });
                
                localStorage.setItem('cv_form_data', JSON.stringify(formData));
                localStorage.setItem('cv_last_save', Date.now().toString());
                
                showSaveNotification('💾 Datos guardados automáticamente');
            } catch (error) {
                console.error('Error saving form data:', error);
            }
        }
        
        function loadSavedData() {
            try {
                const savedData = localStorage.getItem('cv_form_data');
                if (savedData) {
                    const formData = JSON.parse(savedData);
                    
                    Object.keys(formData).forEach(key => {
                        const element = document.getElementById(key) || document.querySelector(`[name="${key}"]`);
                        if (element && formData[key]) {
                            element.value = formData[key];
                            // Trigger change event for Gradio
                            element.dispatchEvent(new Event('input', { bubbles: true }));
                        }
                    });
                    
                    const lastSave = localStorage.getItem('cv_last_save');
                    if (lastSave) {
                        const saveDate = new Date(parseInt(lastSave));
                        showSaveNotification(`📁 Datos restaurados desde ${saveDate.toLocaleString()}`);
                    }
                }
            } catch (error) {
                console.error('Error loading saved data:', error);
            }
        }
        
        function showSaveNotification(message) {
            // Remove existing notifications
            const existing = document.querySelectorAll('.save-notification');
            existing.forEach(el => el.remove());
            
            // Create notification
            const notification = document.createElement('div');
            notification.className = 'save-notification';
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #10b981;
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                z-index: 10000;
                font-size: 14px;
                opacity: 0;
                transform: translateX(100%);
                transition: all 0.3s ease;
            `;
            notification.textContent = message;
            
            document.body.appendChild(notification);
            
            // Animate in
            setTimeout(() => {
                notification.style.opacity = '1';
                notification.style.transform = 'translateX(0)';
            }, 10);
            
            // Animate out
            setTimeout(() => {
                notification.style.opacity = '0';
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }
        
        // Real-time validations
        function setupValidations() {
            // Email validation
            const emailInputs = document.querySelectorAll('input[type="email"], input[placeholder*="email"], input[id*="email"]');
            emailInputs.forEach(input => {
                input.addEventListener('input', function() {
                    const email = this.value;
                    if (email) {
                        const isValid = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);
                        updateValidationFeedback(this, isValid, isValid ? '✅ Email válido' : '❌ Formato de email inválido');
                    } else {
                        clearValidationFeedback(this);
                    }
                });
            });
            
            // Phone validation
            const phoneInputs = document.querySelectorAll('input[type="tel"], input[placeholder*="teléfono"], input[id*="telefono"]');
            phoneInputs.forEach(input => {
                input.addEventListener('input', function() {
                    const phone = this.value;
                    if (phone) {
                        const isValid = /^(\+\d{1,3}[-.\s]?)?\d{3}[-.\s]?\d{3}[-.\s]?\d{3}$/.test(phone.replace(/\s/g, ''));
                        updateValidationFeedback(this, isValid, isValid ? '✅ Teléfono válido' : '❌ Formato de teléfono inválido');
                    } else {
                        clearValidationFeedback(this);
                    }
                });
            });
            
            // LinkedIn validation
            const linkedinInputs = document.querySelectorAll('input[placeholder*="linkedin"], input[id*="linkedin"]');
            linkedinInputs.forEach(input => {
                input.addEventListener('input', function() {
                    const linkedin = this.value;
                    if (linkedin) {
                        const isValid = /^(https?:\/\/)?(www\.)?linkedin\.com\/(in|pub)\/[a-zA-Z0-9-]+\/?$/.test(linkedin);
                        updateValidationFeedback(this, isValid, isValid ? '✅ LinkedIn válido' : '❌ Formato de LinkedIn inválido');
                    } else {
                        clearValidationFeedback(this);
                    }
                });
            });
        }
        
        function updateValidationFeedback(input, isValid, message) {
            clearValidationFeedback(input);
            
            const feedback = document.createElement('div');
            feedback.className = 'validation-feedback';
            feedback.style.cssText = `
                margin-top: 4px;
                font-size: 12px;
                color: ${isValid ? '#10b981' : '#ef4444'};
                display: flex;
                align-items: center;
                gap: 4px;
            `;
            feedback.textContent = message;
            
            input.parentNode.appendChild(feedback);
            input.style.borderColor = isValid ? '#10b981' : '#ef4444';
        }
        
        function clearValidationFeedback(input) {
            const existing = input.parentNode.querySelector('.validation-feedback');
            if (existing) {
                existing.remove();
            }
            input.style.borderColor = '';
        }
        
        // Initialize when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    initializeAutoSave();
                    setupValidations();
                }, 1000);
            });
        } else {
            setTimeout(() => {
                initializeAutoSave();
                setupValidations();
            }, 1000);
        }
    </script>
    """
    
    # Crear la interfaz
    with gr.Blocks(
        css=custom_css,
        title="🚀 Generador Automático de CV con IA - Versión 1.1",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="slate",
            neutral_hue="slate"
        )
    ) as interface:
        
        # Header
        gr.HTML("""
        <div class="main-header">
            <h1>🚀 Generador Automático de CV con IA</h1>
            <p>Crea CVs profesionales de manera inteligente con múltiples plantillas, validación en tiempo real y vista previa en vivo</p>
        </div>
        """)
        
        # Template selector
        with gr.Group(elem_classes=["template-selector"]):
            gr.HTML("<h3>📋 Selecciona tu Plantilla</h3>")
            template = gr.Dropdown(
                choices=[
                    ("🎨 Moderno - Diseño limpio y contemporáneo", "modern"),
                    ("💼 Ejecutivo - Profesional y elegante", "executive"), 
                    ("🎭 Creativo - Vibrante y dinámico", "creative"),
                    ("⚙️ Técnico - Estructurado y detallado", "technical")
                ],
                value="modern",
                label="Plantilla de CV",
                info="Cada plantilla está optimizada para diferentes perfiles profesionales"
            )
        
        # Main form sections
        with gr.Row():
            # Left column
            with gr.Column(scale=1):
                # Personal info
                with gr.Group(elem_classes=["group"]):
                    gr.HTML("<h3>👤 Información Personal</h3>")
                    nombre = gr.Textbox(
                        label="Nombre",
                        placeholder="Tu nombre",
                        info="Nombre completo"
                    )
                    apellidos = gr.Textbox(
                        label="Apellidos", 
                        placeholder="Tus apellidos",
                        info="Apellidos completos"
                    )
                    email = gr.Textbox(
                        label="Email",
                        placeholder="tu.email@ejemplo.com",
                        info="Email de contacto profesional"
                    )
                    telefono = gr.Textbox(
                        label="Teléfono",
                        placeholder="+34 123 456 789",
                        info="Número de teléfono de contacto"
                    )
                    linkedin = gr.Textbox(
                        label="LinkedIn",
                        placeholder="linkedin.com/in/tu-perfil",
                        info="URL de tu perfil de LinkedIn"
                    )
                
                # Professional summary
                with gr.Group(elem_classes=["group"]):
                    gr.HTML("<h3>📝 Resumen Profesional</h3>")
                    resumen_profesional = gr.Textarea(
                        label="Resumen Profesional",
                        placeholder="Breve descripción de tu perfil profesional, objetivos y fortalezas principales...",
                        lines=4,
                        info="Resume tu experiencia y objetivos en 2-3 párrafos"
                    )
            
            # Middle column  
            with gr.Column(scale=1):
                # Experience and Education (moved above Skills)
                with gr.Group(elem_classes=["group"]):
                    gr.HTML("<h3>💼 Experiencia y Formación</h3>")
                    experiencia = gr.Textarea(
                        label="Experiencia Laboral",
                        placeholder="• Empresa - Puesto (Año inicio - Año fin)\n  Descripción de responsabilidades y logros\n\n• Otra empresa...",
                        lines=6,
                        info="Lista tu experiencia laboral más relevante"
                    )
                    formacion = gr.Textarea(
                        label="Formación Académica",
                        placeholder="• Universidad/Centro - Título (Año)\n• Certificaciones relevantes\n• Cursos especializados",
                        lines=4,
                        info="Incluye títulos, certificaciones y formación relevante"
                    )
                
                # Skills and Competencies (moved below Experience)
                with gr.Group(elem_classes=["group"]):
                    gr.HTML("<h3>🎯 Habilidades y Competencias</h3>")
                    habilidades = gr.Textarea(
                        label="Habilidades Técnicas y Blandas",
                        placeholder="• Habilidades técnicas (ej: programación, herramientas)\n• Habilidades blandas (ej: liderazgo, comunicación)\n• Competencias específicas del sector",
                        lines=4,
                        info="Lista tus principales habilidades y competencias"
                    )
            
            # Right column
            with gr.Column(scale=1):
                # Languages
                with gr.Group(elem_classes=["group"]):
                    gr.HTML("<h3>🌍 Idiomas</h3>")
                    idiomas = gr.Textarea(
                        label="Idiomas",
                        placeholder="• Español - Nativo\n• Inglés - Avanzado (C1)\n• Francés - Intermedio (B2)",
                        lines=3,
                        info="Idiomas y nivel de competencia"
                    )
                
                # Certifications
                with gr.Group(elem_classes=["group"]):
                    gr.HTML("<h3>🏆 Certificaciones</h3>")
                    certificaciones = gr.Textarea(
                        label="Certificaciones",
                        placeholder="• Certificación relevante (Entidad, Año)\n• Otra certificación...",
                        lines=3,
                        info="Certificaciones profesionales obtenidas"
                    )
                
                # Projects
                with gr.Group(elem_classes=["group"]):
                    gr.HTML("<h3>🚀 Proyectos Destacados</h3>")
                    proyectos = gr.Textarea(
                        label="Proyectos",
                        placeholder="• Nombre del proyecto - Breve descripción y tecnologías utilizadas\n• Otro proyecto...",
                        lines=3,
                        info="Proyectos relevantes que demuestren tus habilidades"
                    )
                
                # References and extras
                with gr.Group(elem_classes=["group"]):
                    gr.HTML("<h3>📋 Referencias y Extras</h3>")
                    referencias = gr.Textarea(
                        label="Referencias",
                        placeholder="• Nombre - Cargo en Empresa (email/teléfono)\n• Disponibles bajo petición",
                        lines=2,
                        info="Referencias profesionales (opcional)"
                    )
                    extra_fields = gr.Textarea(
                        label="Información Adicional",
                        placeholder="Cualquier información adicional relevante (voluntariado, publicaciones, premios, etc.)",
                        lines=2,
                        info="Información adicional que consideres relevante"
                    )
        
        # Action buttons
        with gr.Row():
            generate_btn = gr.Button(
                "🎨 Generar CV Profesional",
                variant="primary",
                size="lg",
                elem_classes=["generate-button"]
            )
        
        # Output
        with gr.Row():
            with gr.Column(scale=1):
                pdf_output = gr.File(
                    label="📄 Tu CV Generado",
                    file_types=[".pdf"],
                    interactive=False
                )
            with gr.Column(scale=1):
                status_output = gr.Markdown(
                    value="💡 **Completa el formulario y haz clic en 'Generar CV' para crear tu CV profesional**",
                    elem_classes=["status-output"]
                )
        
        # Connect the generate button
        generate_btn.click(
            fn=generate_cv,
            inputs=[
                template, nombre, apellidos, email, telefono, linkedin,
                resumen_profesional, experiencia, formacion, habilidades,
                idiomas, certificaciones, proyectos, referencias, extra_fields
            ],
            outputs=[pdf_output, status_output]
        )
        
        # Add custom JavaScript
        gr.HTML(custom_js)
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;">
            <p style="color: #64748b; font-size: 0.9rem;">
                🤖 <strong>Generador de CV con IA</strong> - Versión 1.1 | 
                ✨ Plantillas múltiples | 🔍 Validación en tiempo real | 💾 Auto-guardado
            </p>
        </div>
        """)
    
    return interface


if __name__ == "__main__":
    try:
        print("🚀 Iniciando Generador de CV con IA...")
        print("📋 Funcionalidades disponibles:")
        print("   • 4 plantillas de CV profesionales")
        print("   • Validación en tiempo real")
        print("   • Auto-guardado automático")
        print("   • Diseño responsive")
        print("   • Vista previa optimizada")
        
        # Crear y lanzar la interfaz
        interface = create_interface()
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True,
            quiet=False
        )
        
    except Exception as e:
        print(f"❌ Error al inicializar la aplicación: {e}")
        import traceback
        traceback.print_exc()