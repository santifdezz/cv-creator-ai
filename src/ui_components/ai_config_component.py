"""
Componente de Configuración de IA - CV Creator AI
Maneja la configuración de proveedores y modelos de IA
"""

import gradio as gr
from typing import Dict, List, Any
from ..config import API_CONFIGS


class AIConfigComponent:
    """Componente para configuración de IA"""
    
    def __init__(self):
        self.components = {}
    
    def render(self) -> Dict[str, Any]:
        """Renderizar el componente de configuración de IA"""
        
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
            
            self.components['api_provider'] = gr.Dropdown(
                choices=provider_choices,
                value="mock",
                label="Proveedor de IA",
                info="💡 Groq es gratis y rápido",
                interactive=True
            )
            
            self.components['modelo_seleccionado'] = gr.Dropdown(
                choices=list(API_CONFIGS["mock"]["models"].keys()),
                value="mock-professional",
                label="Modelo de IA",
                info="Según tu perfil profesional",
                interactive=True
            )
            
            self.components['api_key'] = gr.Textbox(
                label="API Key",
                placeholder="No requerida para el modo simulado",
                type="password",
                visible=False,
                info="🎭 Modo simulado activo",
                lines=1
            )
        
        return self.components
    
    def get_inputs(self) -> List[Any]:
        """Retornar lista de inputs del componente"""
        return [
            self.components['api_provider'],
            self.components['modelo_seleccionado'],
            self.components['api_key']
        ]
    
    def get_change_handlers(self) -> Dict[str, Any]:
        """Retornar handlers de cambio del componente"""
        return {
            'provider_change_models': {
                'fn': self.update_models_dropdown,
                'inputs': [self.components['api_provider']],
                'outputs': [self.components['modelo_seleccionado']]
            },
            'provider_change_key': {
                'fn': self.update_api_key_visibility,
                'inputs': [self.components['api_provider']],
                'outputs': [self.components['api_key']]
            }
        }
    
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