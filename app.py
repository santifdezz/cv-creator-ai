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
    
    def validate_email_realtime(self, email):
        """Valida email en tiempo real"""
        if not email:
            return ""  # Sin mensaje si está vacío
        
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            return '<div style="color: #10b981; font-size: 0.8rem; margin-top: 4px;">✅ Email válido</div>'
        else:
            return '<div style="color: #ef4444; font-size: 0.8rem; margin-top: 4px;">❌ Formato de email incorrecto</div>'
    
    def validate_phone_realtime(self, phone):
        """Valida teléfono en tiempo real y sugiere formato"""
        if not phone:
            return ""  # Sin mensaje si está vacío
        
        import re
        # Limpiar el teléfono
        cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
        
        if len(cleaned_phone) < 8:
            return '<div style="color: #f59e0b; font-size: 0.8rem; margin-top: 4px;">⚠️ Teléfono muy corto (mínimo 8 dígitos)</div>'
        elif len(cleaned_phone) > 15:
            return '<div style="color: #f59e0b; font-size: 0.8rem; margin-top: 4px;">⚠️ Teléfono muy largo (máximo 15 dígitos)</div>'
        elif not cleaned_phone.replace('+', '').isdigit():
            return '<div style="color: #ef4444; font-size: 0.8rem; margin-top: 4px;">❌ Solo números, espacios, + y () permitidos</div>'
        elif cleaned_phone.startswith('+'):
            return '<div style="color: #10b981; font-size: 0.8rem; margin-top: 4px;">✅ Formato internacional correcto</div>'
        elif len(cleaned_phone) == 9 and cleaned_phone.isdigit():
            return f'<div style="color: #3b82f6; font-size: 0.8rem; margin-top: 4px;">💡 Sugerencia: +34 {phone} (España)</div>'
        else:
            return '<div style="color: #10b981; font-size: 0.8rem; margin-top: 4px;">✅ Formato válido</div>'
    
    def validate_linkedin_realtime(self, linkedin):
        """Valida LinkedIn en tiempo real"""
        if not linkedin:
            return ""  # Sin mensaje si está vacío
        
        import re
        
        # Patrones válidos para LinkedIn
        patterns = [
            r'^linkedin\.com/in/[\w\-]+/?$',
            r'^www\.linkedin\.com/in/[\w\-]+/?$',
            r'^https?://(www\.)?linkedin\.com/in/[\w\-]+/?$',
            r'^[\w\-]+$'  # Solo username
        ]
        
        if any(re.match(pattern, linkedin) for pattern in patterns):
            if linkedin.startswith('http'):
                return '<div style="color: #10b981; font-size: 0.8rem; margin-top: 4px;">✅ URL completa válida</div>'
            elif linkedin.startswith('linkedin.com') or linkedin.startswith('www.linkedin'):
                return '<div style="color: #10b981; font-size: 0.8rem; margin-top: 4px;">✅ URL válida</div>'
            else:
                return f'<div style="color: #3b82f6; font-size: 0.8rem; margin-top: 4px;">💡 Se convertirá a: linkedin.com/in/{linkedin}</div>'
        else:
            return '<div style="color: #ef4444; font-size: 0.8rem; margin-top: 4px;">❌ Formato incorrecto. Ej: linkedin.com/in/usuario</div>'
    
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
                         habilidades, idiomas, template_selector, api_provider, modelo_seleccionado, api_key):
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
            
            # Crear PDF con la plantilla seleccionada
            pdf_path = self.pdf_generator.create_cv_pdf(form_data, ai_content, template_selector)
            
            # Formatear mensaje de éxito
            mensaje = format_success_message(nombre, api_provider, modelo_seleccionado, ai_content, template_selector)
            
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
            
            /* Better spacing for mobile */
            .gr-form .form-info {
                font-size: 0.85rem !important;
                margin-top: 0.5rem !important;
            }
            
            /* Mobile-friendly accordions */
            .gr-accordion summary {
                padding: 1.25rem !important;
                font-size: 1rem !important;
                min-height: 48px !important;
            }
        }
        
        /* Small mobile devices */
        @media (max-width: 480px) {
            .gradio-container {
                padding: 0.25rem !important;
            }
            
            .main-header {
                padding: 1rem 0.5rem !important;
            }
            
            .main-header h1 {
                font-size: 1.5rem !important;
            }
            
            .main-header p {
                font-size: 0.9rem !important;
            }
            
            .group,
            .panel,
            .gr-form,
            .gr-panel {
                padding: 0.75rem !important;
                margin-bottom: 0.75rem !important;
            }
            
            .gr-textbox,
            .gr-dropdown,
            .gr-textarea {
                font-size: 16px !important;
                padding: 0.75rem !important;
            }
            
            /* Compact buttons for small screens */
            .gr-button,
            .gr-button-primary {
                padding: 0.75rem 1rem !important;
                font-size: 1rem !important;
            }
        }
        
        /* Tablet landscape optimization */
        @media (min-width: 769px) and (max-width: 1024px) {
            .gradio-container {
                padding: 1rem !important;
            }
            
            .gr-column {
                min-width: 300px !important;
            }
        }
        
        /* Touch device optimizations */
        @media (hover: none) and (pointer: coarse) {
            /* Increase touch targets */
            .gr-button,
            .gr-textbox,
            .gr-dropdown,
            button,
            input,
            select {
                min-height: 44px !important;
                min-width: 44px !important;
            }
            
            /* Remove hover effects on touch devices */
            .gr-button:hover,
            .group:hover,
            .panel:hover {
                transform: none !important;
                box-shadow: var(--shadow-sm) !important;
            }
            
            /* Optimize for touch scrolling */
            body {
                -webkit-overflow-scrolling: touch;
                overflow-scrolling: touch;
            }
        }
        
        /* Landscape mobile optimization */
        @media (max-height: 500px) and (orientation: landscape) {
            .main-header {
                padding: 1rem !important;
                margin-bottom: 1rem !important;
            }
            
            .main-header h1 {
                font-size: 1.5rem !important;
            }
            
            .group,
            .panel,
            .gr-form,
            .gr-panel {
                padding: 0.75rem !important;
                margin-bottom: 0.5rem !important;
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
        
        /* =============================================================================
           WYSIWYG EDITOR STYLES - INTEGRATED
        ============================================================================= */
        
        .wysiwyg-toolbar {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-bottom: none;
            border-radius: var(--border-radius) var(--border-radius) 0 0;
            flex-wrap: wrap;
            margin-bottom: 0;
        }
        
        .toolbar-group {
            display: flex;
            gap: 4px;
            padding-right: 8px;
            border-right: 1px solid var(--border-color);
        }
        
        .toolbar-group:last-child {
            border-right: none;
            padding-right: 0;
        }
        
        .toolbar-btn {
            padding: 6px 10px;
            border: 1px solid var(--border-color);
            background: var(--surface-color);
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            color: var(--text-primary);
            transition: var(--transition);
            min-width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            user-select: none;
        }
        
        .toolbar-btn:hover {
            background: var(--background-color);
            border-color: var(--border-hover);
            transform: translateY(-1px);
        }
        
        .toolbar-btn:active,
        .toolbar-btn.active {
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }
        
        .wysiwyg-container {
            position: relative;
            margin-top: 8px;
        }
        
        .wysiwyg-editor {
            padding: 16px;
            background: var(--surface-color);
            min-height: 120px;
            max-height: 300px;
            overflow-y: auto;
            outline: none;
            line-height: 1.6;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 14px;
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            resize: vertical;
            margin-top: -1px;
            border-top: none;
            border-radius: 0 0 var(--border-radius) var(--border-radius);
        }
        
        .wysiwyg-editor:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }
        
        .wysiwyg-editor:empty:before {
            content: attr(data-placeholder);
            color: var(--text-muted);
            font-style: italic;
            pointer-events: none;
        }
        
        .wysiwyg-editor p {
            margin: 0 0 8px 0;
        }
        
        .wysiwyg-editor p:last-child {
            margin-bottom: 0;
        }
        
        .wysiwyg-editor ul,
        .wysiwyg-editor ol {
            margin: 8px 0;
            padding-left: 24px;
        }
        
        .wysiwyg-editor li {
            margin: 4px 0;
        }
        
        .wysiwyg-editor strong {
            font-weight: 600;
        }
        
        .wysiwyg-editor em {
            font-style: italic;
        }
        
        .wysiwyg-editor u {
            text-decoration: underline;
        }
        
        /* =============================================================================
           DRAG AND DROP STYLES - INTEGRATED
        ============================================================================= */
        
        .draggable-section {
            background: var(--surface-color) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: var(--border-radius) !important;
            margin-bottom: 16px !important;
            overflow: hidden !important;
            transition: var(--transition) !important;
            position: relative !important;
        }
        
        .draggable-section.dragging {
            opacity: 0.5 !important;
            transform: rotate(2deg) !important;
            box-shadow: var(--shadow-lg) !important;
            z-index: 1000 !important;
        }
        
        .draggable-section.drag-over {
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1) !important;
        }
        
        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 20px;
            background: linear-gradient(135deg, var(--background-color), #f1f5f9);
            border-bottom: 1px solid var(--border-color);
            cursor: move;
            user-select: none;
            transition: var(--transition);
        }
        
        .section-header:hover {
            background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
        }
        
        .section-header.dragging {
            cursor: grabbing;
        }
        
        .section-title {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 600;
            color: var(--text-primary);
            font-size: 16px;
        }
        
        .drag-icon {
            color: var(--text-muted);
            font-size: 14px;
            cursor: grab;
            opacity: 0.6;
            transition: var(--transition);
        }
        
        .section-header:hover .drag-icon {
            opacity: 1;
            color: var(--primary-color);
        }
        
        .section-icon {
            font-size: 18px;
        }
        
        .collapse-btn {
            background: none;
            border: none;
            padding: 8px;
            cursor: pointer;
            border-radius: 4px;
            transition: var(--transition);
            color: var(--text-secondary);
        }
        
        .collapse-btn:hover {
            background: rgba(0, 0, 0, 0.05);
            color: var(--text-primary);
        }
        
        .collapse-btn span {
            display: inline-block;
            transition: transform 0.3s ease;
        }
        
        .collapse-btn.collapsed span {
            transform: rotate(-90deg);
        }
        
        .section-content {
            padding: 20px !important;
            transition: var(--transition) !important;
        }
        
        .section-content.collapsed {
            display: none !important;
        }
        
        .drag-placeholder {
            height: 60px;
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(37, 99, 235, 0.05));
            border: 2px dashed var(--primary-color);
            border-radius: var(--border-radius);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary-color);
            font-weight: 500;
            opacity: 0;
            transform: scale(0.95);
            transition: var(--transition);
        }
        
        .drag-placeholder.active {
            opacity: 1;
            transform: scale(1);
        }
        
        /* Enhanced section styling */
        .enhanced-section {
            position: relative;
        }
        
        .enhanced-section .group {
            border: 2px solid var(--border-color) !important;
            border-radius: var(--border-radius-lg) !important;
            overflow: visible !important;
        }
        
        .enhanced-section h3 {
            background: linear-gradient(135deg, var(--primary-color), #3b82f6) !important;
            color: white !important;
            margin: -24px -24px 20px -24px !important;
            padding: 16px 24px !important;
            border-radius: var(--border-radius-lg) var(--border-radius-lg) 0 0 !important;
            position: relative !important;
        }
        
        .enhanced-section h3:after {
            content: '⋮⋮';
            position: absolute;
            right: 16px;
            top: 50%;
            transform: translateY(-50%);
            opacity: 0.7;
            font-size: 14px;
            cursor: grab;
        }
        
        /* Mobile optimizations for new components */
        @media (max-width: 768px) {
            .wysiwyg-toolbar {
                padding: 6px 8px;
                gap: 4px;
            }
            
            .toolbar-btn {
                min-width: 28px;
                height: 28px;
                font-size: 11px;
                padding: 4px 6px;
            }
            
            .wysiwyg-editor {
                padding: 12px;
                font-size: 13px;
            }
            
            .section-header {
                padding: 12px 16px;
            }
            
            .section-title {
                font-size: 14px;
                gap: 8px;
            }
            
            .drag-icon {
                font-size: 12px;
            }
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
                            lines=1,
                            elem_id="nombre_input"
                        )
                        
                        with gr.Row():
                            email = gr.Textbox(
                                label="Email *",
                                placeholder="maria.garcia@email.com",
                                info="Email profesional preferiblemente",
                                lines=1,
                                elem_id="email_input"
                            )
                            telefono = gr.Textbox(
                                label="Teléfono *",
                                placeholder="+34 666 123 456",
                                info="Con código de país",
                                lines=1,
                                elem_id="telefono_input"
                            )
                        
                        # Indicadores de validación
                        with gr.Row():
                            email_validation = gr.HTML("", elem_id="email_validation")
                            phone_validation = gr.HTML("", elem_id="phone_validation")
                        
                        with gr.Row():
                            linkedin = gr.Textbox(
                                label="LinkedIn (Opcional)",
                                placeholder="linkedin.com/in/maria-garcia",
                                info="Solo el nombre de usuario o URL completa",
                                lines=1,
                                elem_id="linkedin_input"
                            )
                            ubicacion = gr.Textbox(
                                label="Ubicación (Opcional)",
                                placeholder="Madrid, España",
                                info="Ciudad y país donde resides",
                                lines=1,
                                elem_id="ubicacion_input"
                            )
                        
                        # Indicador de validación LinkedIn
                        linkedin_validation = gr.HTML("", elem_id="linkedin_validation")
                    
                    # Selector de plantilla CV
                    with gr.Group():
                        gr.Markdown("### 🎨 **Plantilla de CV**")
                        
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
                            info="🎯 Elige la plantilla que mejor se adapte a tu perfil profesional",
                            interactive=True
                        )
                        
                        # Vista previa de plantillas
                        gr.HTML("""
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-top: 12px;">
                            <div style="padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; text-align: center; background: linear-gradient(135deg, #f8fafc, #e2e8f0);">
                                <strong style="color: #2563eb;">🎨 Moderna</strong><br>
                                <small style="color: #6b7280;">Limpia y profesional</small>
                            </div>
                            <div style="padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; text-align: center; background: linear-gradient(135deg, #f9fafb, #f3f4f6);">
                                <strong style="color: #374151;">👔 Ejecutiva</strong><br>
                                <small style="color: #6b7280;">Tradicional y formal</small>
                            </div>
                            <div style="padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; text-align: center; background: linear-gradient(135deg, #fef7ff, #f3e8ff);">
                                <strong style="color: #7c3aed;">🌈 Creativa</strong><br>
                                <small style="color: #6b7280;">Colorida y llamativa</small>
                            </div>
                            <div style="padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; text-align: center; background: linear-gradient(135deg, #f0fdf4, #dcfce7);">
                                <strong style="color: #16a34a;">💻 Técnica</strong><br>
                                <small style="color: #6b7280;">Estructurada y clara</small>
                            </div>
                        </div>
                        """)
                    
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
                    
                    # Experiencia y educación (movido arriba)
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
                    
                    # Habilidades y competencias (movido abajo)
                    with gr.Group():
                        gr.Markdown("### 🔧 **Habilidades y Competencias**")
                        
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
                
                # Columna derecha: Generación y acción (30%)
                with gr.Column(scale=3, min_width=300):
                    gr.Markdown("## � Generar tu CV")
                    
                    # Información de ATS y botones consolidados
                    gr.HTML("""
                    <div style="background: linear-gradient(135deg, #fef3c7, #fde68a); padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                        <div style="text-align: center;">
                            <div style="font-size: 1.1rem; font-weight: 600; color: #92400e;">🎯 Optimización ATS Automática</div>
                            <div style="font-size: 0.9rem; color: #a16207; margin-top: 4px;">Palabras clave técnicas añadidas automáticamente según tu sector</div>
                        </div>
                    </div>
                    """)
                    
                    # Botones de acción consolidados en fila
                    with gr.Row():
                        generar_btn = gr.Button(
                            "🤖 Generar CV",
                            variant="primary",
                            size="lg",
                            scale=2,
                            elem_id="generate_button"
                        )
                        
                        live_preview_toggle = gr.Button(
                            "👁️ Vista Previa",
                            variant="secondary", 
                            size="lg",
                            scale=1,
                            elem_id="live_preview_toggle"
                        )
                    
                    # Tips consolidados en accordion
                    with gr.Accordion("💡 Tips para un CV Exitoso", open=False):
                        gr.Markdown("""
                        **✨ Consejos clave:**
                        - **Sé específico**: Usa números y métricas
                        - **Personaliza**: Adapta cada CV a la oferta  
                        - **Palabras clave**: Incluye términos del sector
                        - **Formato limpio**: Usa viñetas y espacios
                        - **Longitud ideal**: 1-2 páginas máximo
                        """)
                    
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
                    habilidades, idiomas, template_selector, api_provider, modelo_seleccionado, api_key
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
            
            # Auto-save notification
            gr.HTML("""
            <script>
            // =============================================================================
            // WYSIWYG EDITOR AND DRAG-DROP FUNCTIONALITY - INTEGRATED
            // =============================================================================
            
            // WYSIWYG Editor Class
            class WYSIWYGEditor {
                constructor(container) {
                    this.container = container;
                    this.editor = null;
                    this.toolbar = null;
                    this.init();
                }
                
                init() {
                    this.createToolbar();
                    this.createEditor();
                    this.attachEvents();
                }
                
                createToolbar() {
                    this.toolbar = document.createElement('div');
                    this.toolbar.className = 'wysiwyg-toolbar';
                    this.toolbar.innerHTML = `
                        <div class="toolbar-group">
                            <button class="toolbar-btn" data-command="bold" title="Negrita">
                                <strong>B</strong>
                            </button>
                            <button class="toolbar-btn" data-command="italic" title="Cursiva">
                                <em>I</em>
                            </button>
                            <button class="toolbar-btn" data-command="underline" title="Subrayado">
                                <u>U</u>
                            </button>
                        </div>
                        <div class="toolbar-group">
                            <button class="toolbar-btn" data-command="insertOrderedList" title="Lista numerada">
                                1.
                            </button>
                            <button class="toolbar-btn" data-command="insertUnorderedList" title="Lista con viñetas">
                                •
                            </button>
                        </div>
                        <div class="toolbar-group">
                            <button class="toolbar-btn" data-command="undo" title="Deshacer">
                                ↶
                            </button>
                            <button class="toolbar-btn" data-command="redo" title="Rehacer">
                                ↷
                            </button>
                        </div>
                    `;
                    this.container.appendChild(this.toolbar);
                }
                
                createEditor() {
                    this.editor = document.createElement('div');
                    this.editor.className = 'wysiwyg-editor';
                    this.editor.contentEditable = true;
                    this.editor.setAttribute('data-placeholder', 'Escribe aquí...');
                    this.container.appendChild(this.editor);
                }
                
                attachEvents() {
                    // Toolbar button events
                    this.toolbar.addEventListener('click', (e) => {
                        if (e.target.classList.contains('toolbar-btn')) {
                            e.preventDefault();
                            const command = e.target.getAttribute('data-command');
                            this.executeCommand(command);
                        }
                    });
                    
                    // Editor events
                    this.editor.addEventListener('input', () => {
                        this.updateToolbarState();
                        this.syncWithGradio();
                    });
                    
                    this.editor.addEventListener('keydown', (e) => {
                        if (e.ctrlKey || e.metaKey) {
                            switch(e.key) {
                                case 'b':
                                    e.preventDefault();
                                    this.executeCommand('bold');
                                    break;
                                case 'i':
                                    e.preventDefault();
                                    this.executeCommand('italic');
                                    break;
                                case 'u':
                                    e.preventDefault();
                                    this.executeCommand('underline');
                                    break;
                            }
                        }
                    });
                }
                
                executeCommand(command) {
                    document.execCommand(command, false, null);
                    this.editor.focus();
                    this.updateToolbarState();
                    this.syncWithGradio();
                }
                
                updateToolbarState() {
                    const buttons = this.toolbar.querySelectorAll('.toolbar-btn');
                    buttons.forEach(button => {
                        const command = button.getAttribute('data-command');
                        if (['bold', 'italic', 'underline', 'insertOrderedList', 'insertUnorderedList'].includes(command)) {
                            if (document.queryCommandState(command)) {
                                button.classList.add('active');
                            } else {
                                button.classList.remove('active');
                            }
                        }
                    });
                }
                
                syncWithGradio() {
                    // Find associated Gradio textarea and update it
                    const textarea = this.container.parentElement.querySelector('textarea');
                    if (textarea) {
                        textarea.value = this.getPlainText();
                        textarea.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                }
                
                getPlainText() {
                    return this.editor.innerText || '';
                }
                
                getHTML() {
                    return this.editor.innerHTML;
                }
                
                setContent(content) {
                    this.editor.innerHTML = content;
                }
            }
            
            // Drag and Drop Manager Class
            class DragDropManager {
                constructor() {
                    this.sections = [];
                    this.draggedElement = null;
                    this.placeholder = null;
                    this.init();
                }
                
                init() {
                    this.createSections();
                    this.attachEvents();
                    this.loadSectionOrder();
                }
                
                createSections() {
                    // Find all section containers
                    const containers = document.querySelectorAll('.gradio-group, .gradio-accordion');
                    containers.forEach((container, index) => {
                        if (this.shouldMakeDraggable(container)) {
                            this.enhanceSection(container, index);
                        }
                    });
                }
                
                shouldMakeDraggable(element) {
                    // Only make sections draggable if they contain form elements
                    return element.querySelector('input, textarea, select') !== null;
                }
                
                enhanceSection(container, index) {
                    if (container.classList.contains('enhanced-section')) return;
                    
                    container.classList.add('enhanced-section', 'draggable-section');
                    container.setAttribute('data-section-id', index);
                    
                    // Create section header
                    const header = document.createElement('div');
                    header.className = 'section-header';
                    header.innerHTML = `
                        <div class="section-title">
                            <span class="drag-icon">⋮⋮</span>
                            <span class="section-icon">${this.getSectionIcon(container)}</span>
                            <span>${this.getSectionTitle(container)}</span>
                        </div>
                        <button class="collapse-btn" type="button">
                            <span>▼</span>
                        </button>
                    `;
                    
                    // Wrap content
                    const content = document.createElement('div');
                    content.className = 'section-content';
                    while (container.firstChild) {
                        content.appendChild(container.firstChild);
                    }
                    
                    container.appendChild(header);
                    container.appendChild(content);
                    
                    this.sections.push({
                        element: container,
                        header: header,
                        content: content,
                        id: index,
                        collapsed: false
                    });
                }
                
                getSectionIcon(container) {
                    const text = container.textContent.toLowerCase();
                    if (text.includes('personal') || text.includes('contacto')) return '👤';
                    if (text.includes('experiencia') || text.includes('trabajo')) return '💼';
                    if (text.includes('educación') || text.includes('formación')) return '🎓';
                    if (text.includes('habilidades') || text.includes('skills')) return '🔧';
                    if (text.includes('idiomas') || text.includes('languages')) return '🌐';
                    if (text.includes('certificaciones') || text.includes('certificados')) return '📜';
                    return '📄';
                }
                
                getSectionTitle(container) {
                    const label = container.querySelector('label');
                    if (label) return label.textContent.trim();
                    
                    const heading = container.querySelector('h1, h2, h3, h4, h5, h6');
                    if (heading) return heading.textContent.trim();
                    
                    return 'Sección';
                }
                
                attachEvents() {
                    document.addEventListener('mousedown', this.handleMouseDown.bind(this));
                    document.addEventListener('mousemove', this.handleMouseMove.bind(this));
                    document.addEventListener('mouseup', this.handleMouseUp.bind(this));
                    document.addEventListener('click', this.handleClick.bind(this));
                }
                
                handleMouseDown(e) {
                    const header = e.target.closest('.section-header');
                    if (!header || e.target.closest('.collapse-btn')) return;
                    
                    this.draggedElement = header.parentElement;
                    this.draggedElement.classList.add('dragging');
                    header.classList.add('dragging');
                    
                    this.createPlaceholder();
                    e.preventDefault();
                }
                
                handleMouseMove(e) {
                    if (!this.draggedElement) return;
                    
                    const sections = document.querySelectorAll('.draggable-section:not(.dragging)');
                    let targetSection = null;
                    let insertAfter = false;
                    
                    sections.forEach(section => {
                        const rect = section.getBoundingClientRect();
                        const centerY = rect.top + rect.height / 2;
                        
                        if (e.clientY < centerY && e.clientY > rect.top) {
                            targetSection = section;
                            insertAfter = false;
                        } else if (e.clientY > centerY && e.clientY < rect.bottom) {
                            targetSection = section;
                            insertAfter = true;
                        }
                    });
                    
                    this.updatePlaceholder(targetSection, insertAfter);
                }
                
                handleMouseUp(e) {
                    if (!this.draggedElement) return;
                    
                    this.completeDrop();
                    this.draggedElement.classList.remove('dragging');
                    this.draggedElement.querySelector('.section-header').classList.remove('dragging');
                    this.draggedElement = null;
                    this.removePlaceholder();
                    
                    this.saveSectionOrder();
                }
                
                handleClick(e) {
                    const collapseBtn = e.target.closest('.collapse-btn');
                    if (collapseBtn) {
                        e.preventDefault();
                        this.toggleSection(collapseBtn);
                    }
                }
                
                createPlaceholder() {
                    this.placeholder = document.createElement('div');
                    this.placeholder.className = 'drag-placeholder';
                    this.placeholder.textContent = 'Suelta aquí';
                }
                
                updatePlaceholder(targetSection, insertAfter) {
                    if (!targetSection) {
                        this.removePlaceholder();
                        return;
                    }
                    
                    this.placeholder.classList.add('active');
                    
                    if (insertAfter) {
                        targetSection.parentNode.insertBefore(this.placeholder, targetSection.nextSibling);
                    } else {
                        targetSection.parentNode.insertBefore(this.placeholder, targetSection);
                    }
                }
                
                completeDrop() {
                    if (this.placeholder && this.placeholder.parentNode) {
                        this.placeholder.parentNode.insertBefore(this.draggedElement, this.placeholder);
                    }
                }
                
                removePlaceholder() {
                    if (this.placeholder && this.placeholder.parentNode) {
                        this.placeholder.parentNode.removeChild(this.placeholder);
                    }
                }
                
                toggleSection(button) {
                    const section = button.closest('.draggable-section');
                    const content = section.querySelector('.section-content');
                    const icon = button.querySelector('span');
                    
                    if (content.classList.contains('collapsed')) {
                        content.classList.remove('collapsed');
                        button.classList.remove('collapsed');
                        icon.textContent = '▼';
                    } else {
                        content.classList.add('collapsed');
                        button.classList.add('collapsed');
                        icon.textContent = '▶';
                    }
                }
                
                saveSectionOrder() {
                    const order = Array.from(document.querySelectorAll('.draggable-section')).map(section => 
                        section.getAttribute('data-section-id')
                    );
                    localStorage.setItem('cv_section_order', JSON.stringify(order));
                }
                
                loadSectionOrder() {
                    try {
                        const savedOrder = localStorage.getItem('cv_section_order');
                        if (savedOrder) {
                            const order = JSON.parse(savedOrder);
                            this.applySectionOrder(order);
                        }
                    } catch (error) {
                        console.error('Error loading section order:', error);
                    }
                }
                
                applySectionOrder(order) {
                    const container = document.querySelector('.gradio-container');
                    if (!container) return;
                    
                    order.forEach(sectionId => {
                        const section = document.querySelector(`[data-section-id="${sectionId}"]`);
                        if (section) {
                            container.appendChild(section);
                        }
                    });
                }
            }
            
            // Enhanced initialization
            function initializeEnhancements() {
                // Initialize WYSIWYG editors
                const textareas = document.querySelectorAll('textarea[placeholder*="experiencia"], textarea[placeholder*="descripción"], textarea[placeholder*="objetivo"]');
                textareas.forEach(textarea => {
                    if (!textarea.parentElement.querySelector('.wysiwyg-toolbar')) {
                        const container = document.createElement('div');
                        container.className = 'wysiwyg-container';
                        textarea.parentElement.insertBefore(container, textarea);
                        textarea.style.display = 'none'; // Hide original textarea
                        
                        const editor = new WYSIWYGEditor(container);
                        editor.setContent(textarea.value);
                    }
                });
                
                // Initialize drag and drop
                if (!window.dragDropManager) {
                    window.dragDropManager = new DragDropManager();
                }
                
                console.log('✅ Enhanced UI components initialized');
            }
            
            // Initialize when DOM is ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', function() {
                    setTimeout(initializeEnhancements, 2000);
                });
            } else {
                setTimeout(initializeEnhancements, 2000);
            }
            
            // Re-initialize when content changes
            const observer = new MutationObserver((mutations) => {
                let shouldReinit = false;
                mutations.forEach((mutation) => {
                    if (mutation.addedNodes.length > 0) {
                        mutation.addedNodes.forEach((node) => {
                            if (node.nodeType === 1 && (node.querySelector('textarea') || node.classList.contains('gradio-group'))) {
                                shouldReinit = true;
                            }
                        });
                    }
                });
                
                if (shouldReinit) {
                    setTimeout(initializeEnhancements, 1000);
                }
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
            
            // Enhanced Auto-save functionality for CV Generator
            (function() {
                const STORAGE_KEY = 'cv_generator_autosave';
                const SAVE_INTERVAL = 30000; // 30 seconds
                
                let saveTimer = null;
                let hasUnsavedChanges = false;
                
                function saveFormData() {
                    try {
                        const formData = {};
                        const inputs = document.querySelectorAll('input[type="text"], textarea, select');
                        
                        inputs.forEach(input => {
                            if (input.value && input.value.trim()) {
                                // Use placeholder as key if no ID available
                                let key = input.id || input.placeholder || input.name || 'unknown';
                                key = key.toLowerCase().replace(/[^a-z0-9]/g, '_');
                                formData[key] = input.value.trim();
                            }
                        });
                        
                        if (Object.keys(formData).length > 0) {
                            formData.timestamp = new Date().toISOString();
                            formData.version = '1.1';
                            localStorage.setItem(STORAGE_KEY, JSON.stringify(formData));
                            hasUnsavedChanges = false;
                            console.log('📝 Form auto-saved at', new Date().toLocaleTimeString());
                        }
                    } catch (error) {
                        console.error('❌ Auto-save failed:', error);
                    }
                }
                
                function loadSavedData() {
                    try {
                        const savedData = localStorage.getItem(STORAGE_KEY);
                        if (!savedData) return false;
                        
                        const data = JSON.parse(savedData);
                        const savedTime = new Date(data.timestamp);
                        const hoursSince = (new Date() - savedTime) / (1000 * 60 * 60);
                        
                        // Only show if saved within last 24 hours
                        if (hoursSince < 24) {
                            showAutoSaveNotification(savedTime, data);
                            return true;
                        }
                    } catch (error) {
                        console.error('❌ Failed to load saved data:', error);
                    }
                    return false;
                }
                
                function showAutoSaveNotification(savedTime, data) {
                    const notification = document.createElement('div');
                    notification.innerHTML = `
                        <div style="background: linear-gradient(135deg, #fef3c7, #fde68a); border: 1px solid #f59e0b; padding: 1rem; border-radius: 8px; margin: 1rem 0; position: relative; animation: slideIn 0.3s ease;">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <span style="font-size: 1.2rem;">💾</span>
                                <div>
                                    <strong style="color: #92400e;">Datos guardados encontrados</strong><br>
                                    <small style="color: #a16207;">Guardado: ${savedTime.toLocaleString()}</small>
                                </div>
                                <button onclick="this.parentElement.parentElement.remove()" 
                                        style="position: absolute; top: 8px; right: 12px; background: none; border: none; font-size: 1.2rem; cursor: pointer; color: #92400e;">×</button>
                            </div>
                        </div>
                    `;
                    
                    // Insert at the top of the container
                    setTimeout(() => {
                        const container = document.querySelector('.gradio-container');
                        if (container) {
                            container.insertBefore(notification, container.firstChild);
                            // Auto-hide after 10 seconds
                            setTimeout(() => {
                                if (notification.parentNode) {
                                    notification.style.animation = 'slideOut 0.3s ease';
                                    setTimeout(() => notification.remove(), 300);
                                }
                            }, 10000);
                        }
                    }, 1000);
                }
                
                function setupAutoSave() {
                    // Set up periodic save
                    saveTimer = setInterval(saveFormData, SAVE_INTERVAL);
                    
                    // Save on input changes (debounced)
                    let changeTimer = null;
                    document.addEventListener('input', function(e) {
                        if (e.target.matches('input[type="text"], textarea, select')) {
                            hasUnsavedChanges = true;
                            clearTimeout(changeTimer);
                            changeTimer = setTimeout(saveFormData, 3000); // Save 3 seconds after last change
                        }
                    });
                    
                    // Save before page unload
                    window.addEventListener('beforeunload', function(e) {
                        if (hasUnsavedChanges) {
                            saveFormData();
                        }
                    });
                    
                    // Load saved data on startup
                    setTimeout(loadSavedData, 2000);
                    
                    console.log('🔄 Auto-save system initialized');
                }
                
                // CSS animations
                const style = document.createElement('style');
                style.textContent = `
                    @keyframes slideIn {
                        from { opacity: 0; transform: translateY(-20px); }
                        to { opacity: 1; transform: translateY(0); }
                    }
                    @keyframes slideOut {
                        from { opacity: 1; transform: translateY(0); }
                        to { opacity: 0; transform: translateY(-20px); }
                    }
                `;
                document.head.appendChild(style);
                
                // Initialize when DOM is ready
                if (document.readyState === 'loading') {
                    document.addEventListener('DOMContentLoaded', setupAutoSave);
                } else {
                    setTimeout(setupAutoSave, 1000);
                }
            })();
            
            // Live PDF Preview functionality
            (function() {
                let previewTimeout;
                let isPreviewEnabled = false;
                
                function enableLivePreview() {
                    isPreviewEnabled = true;
                    updatePreviewButton();
                    showNotification('👁️ Vista previa en vivo activada', 'success');
                }
                
                function disableLivePreview() {
                    isPreviewEnabled = false;
                    updatePreviewButton();
                    clearTimeout(previewTimeout);
                    showNotification('🔴 Vista previa en vivo desactivada', 'info');
                }
                
                function updatePreviewButton() {
                    const button = document.querySelector('#live_preview_toggle button');
                    if (button) {
                        button.textContent = isPreviewEnabled ? '🔴 Desactivar Vista Previa' : '👁️ Activar Vista Previa';
                        button.style.backgroundColor = isPreviewEnabled ? '#ef4444' : '#10b981';
                    }
                }
                
                function schedulePreviewUpdate() {
                    if (!isPreviewEnabled) return;
                    
                    clearTimeout(previewTimeout);
                    previewTimeout = setTimeout(() => {
                        triggerPreviewUpdate();
                    }, 3000); // Update preview 3 seconds after user stops typing
                }
                
                function triggerPreviewUpdate() {
                    const generateButton = document.querySelector('#generate_button button');
                    if (generateButton && isPreviewEnabled) {
                        // Show preview indicator
                        const originalText = generateButton.textContent;
                        generateButton.textContent = '🔄 Actualizando vista previa...';
                        generateButton.style.backgroundColor = '#f59e0b';
                        
                        // Trigger CV generation
                        generateButton.click();
                        
                        // Reset button after a delay
                        setTimeout(() => {
                            if (generateButton.textContent.includes('Actualizando')) {
                                generateButton.textContent = originalText;
                                generateButton.style.backgroundColor = '';
                            }
                        }, 3000);
                    }
                }
                
                // Live preview input monitoring
                function setupLivePreview() {
                    const inputs = document.querySelectorAll('input, textarea, select');
                    inputs.forEach(input => {
                        input.addEventListener('input', schedulePreviewUpdate);
                        input.addEventListener('change', schedulePreviewUpdate);
                    });
                    
                    // Monitor for new inputs added dynamically
                    const observer = new MutationObserver((mutations) => {
                        mutations.forEach((mutation) => {
                            mutation.addedNodes.forEach((node) => {
                                if (node.nodeType === 1) { // Element node
                                    const newInputs = node.querySelectorAll('input, textarea, select');
                                    newInputs.forEach(input => {
                                        input.addEventListener('input', schedulePreviewUpdate);
                                        input.addEventListener('change', schedulePreviewUpdate);
                                    });
                                }
                            });
                        });
                    });
                    
                    observer.observe(document.body, {
                        childList: true,
                        subtree: true
                    });
                }
                
                // Make functions available globally for Gradio events
                window.enableLivePreview = enableLivePreview;
                window.disableLivePreview = disableLivePreview;
                
                // Initialize live preview when page loads
                if (document.readyState === 'loading') {
                    document.addEventListener('DOMContentLoaded', function() {
                        setTimeout(setupLivePreview, 1000);
                        setTimeout(updatePreviewButton, 1500);
                    });
                } else {
                    setTimeout(setupLivePreview, 1000);
                    setTimeout(updatePreviewButton, 1500);
                }
            })();
            </script>
            """)
            
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