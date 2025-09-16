"""
Componente de Generación - CV Creator AI
Maneja la zona de generación, botones de acción y resultados
"""

import gradio as gr
from typing import Dict, List, Any, Optional


class GenerationComponent:
    """Componente para la zona de generación y resultados"""
    
    def __init__(self):
        self.components = {}
    
    def render(self) -> Dict[str, Any]:
        """Renderizar el componente de generación"""
        
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
            self.components['generar_btn'] = gr.Button(
                "🤖 Generar CV",
                variant="primary",
                size="lg",
                scale=1,
                elem_id="generate_button"
            )
        
        with gr.Row():
            self.components['live_preview_toggle'] = gr.Button(
                "👁️ Vista Previa en Vivo",
                variant="secondary",
                size="sm",
                scale=1,
                elem_id="live_preview_toggle"
            )
        
        # Indicador de progreso
        self.components['progress_html'] = gr.HTML(visible=False)
        
        return self.components
    
    def render_results_area(self) -> Dict[str, Any]:
        """Renderizar área de resultados"""
        results = {}
        
        # ===================================================================
        # ÁREA DE RESULTADOS (Ancho completo)
        # ===================================================================
        gr.Markdown("---")
        gr.Markdown("## 📄 **Resultado Generado**")
        
        with gr.Row():
            with gr.Column(scale=2):
                results['resultado_texto'] = gr.Markdown()
            
            with gr.Column(scale=1):
                results['archivo_descarga'] = gr.File(
                    label="📁 **Descargar CV (PDF)**",
                    visible=True,
                    height=120
                )
        
        return results
    
    def get_generation_inputs(self) -> List[Any]:
        """Retornar inputs necesarios para la generación"""
        return [self.components['generar_btn']]
    
    def get_live_preview_handlers(self) -> Dict[str, Any]:
        """Retornar handlers de vista previa en vivo"""
        live_preview_state = gr.State(False)
        
        def toggle_live_preview(current_state):
            new_state = not current_state
            if new_state:
                return new_state, "🔴 Desactivar Vista Previa"
            else:
                return new_state, "👁️ Activar Vista Previa"
        
        return {
            'state': live_preview_state,
            'toggle_handler': {
                'fn': toggle_live_preview,
                'inputs': [live_preview_state],
                'outputs': [live_preview_state, self.components['live_preview_toggle']]
            }
        }