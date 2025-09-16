"""
UI Components Module - Clean Architecture
Componentes modulares para la interfaz de usuario del generador de CV
"""

from abc import ABC, abstractmethod
import gradio as gr
from typing import Dict, Any, List, Tuple


class UIComponent(ABC):
    """Clase base abstracta para componentes de UI"""
    
    def __init__(self):
        self.component = None
        self.validation_component = None
    
    @abstractmethod
    def render(self) -> gr.components.Component:
        """Renderiza el componente de UI"""
        pass
    
    @abstractmethod
    def get_validation_events(self) -> List[Tuple]:
        """Retorna eventos de validación del componente"""
        pass


class PersonalInfoComponent(UIComponent):
    """Componente para información personal"""
    
    def render(self) -> Dict[str, gr.components.Component]:
        """Renderiza los campos de información personal"""
        with gr.Group(elem_classes=["group"]):
            gr.HTML("<h3>👤 Información Personal</h3>")
            
            components = {}
            
            components['nombre'] = gr.Textbox(
                label="Nombre",
                placeholder="Tu nombre",
                info="Nombre completo",
                elem_id="nombre_input"
            )
            
            components['apellidos'] = gr.Textbox(
                label="Apellidos", 
                placeholder="Tus apellidos",
                info="Apellidos completos",
                elem_id="apellidos_input"
            )
            
            with gr.Row():
                components['email'] = gr.Textbox(
                    label="Email",
                    placeholder="tu.email@ejemplo.com",
                    info="Email de contacto profesional",
                    elem_id="email_input"
                )
                components['telefono'] = gr.Textbox(
                    label="Teléfono",
                    placeholder="+34 123 456 789",
                    info="Número de teléfono de contacto",
                    elem_id="telefono_input"
                )
            
            with gr.Row():
                components['linkedin'] = gr.Textbox(
                    label="LinkedIn (Opcional)",
                    placeholder="linkedin.com/in/tu-perfil",
                    info="Solo el nombre de usuario o URL completa",
                    elem_id="linkedin_input"
                )
                components['ubicacion'] = gr.Textbox(
                    label="Ubicación (Opcional)",
                    placeholder="Madrid, España",
                    info="Ciudad y país donde resides",
                    elem_id="ubicacion_input"
                )
            
            # Componentes de validación
            components['email_validation'] = gr.HTML("", elem_id="email_validation")
            components['phone_validation'] = gr.HTML("", elem_id="phone_validation")
            components['linkedin_validation'] = gr.HTML("", elem_id="linkedin_validation")
            
        return components
    
    def get_validation_events(self) -> List[Tuple]:
        """Retorna eventos de validación para información personal"""
        return [
            ('email', 'email_validation', 'validate_email_realtime'),
            ('telefono', 'phone_validation', 'validate_phone_realtime'),
            ('linkedin', 'linkedin_validation', 'validate_linkedin_realtime')
        ]


class RichTextComponent(UIComponent):
    """Componente avanzado con editor WYSIWYG"""
    
    def __init__(self, label: str, placeholder: str, info: str, elem_id: str, lines: int = 4):
        super().__init__()
        self.label = label
        self.placeholder = placeholder
        self.info = info
        self.elem_id = elem_id
        self.lines = lines
    
    def render(self) -> gr.components.Component:
        """Renderiza un editor de texto enriquecido"""
        with gr.Column():
            # Toolbar del editor WYSIWYG
            gr.HTML(f"""
            <div class="wysiwyg-toolbar" data-target="{self.elem_id}">
                <div class="toolbar-group">
                    <button type="button" class="toolbar-btn" data-command="bold" title="Negrita">
                        <strong>B</strong>
                    </button>
                    <button type="button" class="toolbar-btn" data-command="italic" title="Cursiva">
                        <em>I</em>
                    </button>
                    <button type="button" class="toolbar-btn" data-command="underline" title="Subrayado">
                        <u>U</u>
                    </button>
                </div>
                <div class="toolbar-group">
                    <button type="button" class="toolbar-btn" data-command="insertUnorderedList" title="Lista con viñetas">
                        • Lista
                    </button>
                    <button type="button" class="toolbar-btn" data-command="insertOrderedList" title="Lista numerada">
                        1. Lista
                    </button>
                </div>
                <div class="toolbar-group">
                    <button type="button" class="toolbar-btn" data-command="undo" title="Deshacer">
                        ↶ Deshacer
                    </button>
                    <button type="button" class="toolbar-btn" data-command="redo" title="Rehacer">
                        ↷ Rehacer
                    </button>
                </div>
            </div>
            """, elem_id=f"{self.elem_id}_toolbar")
            
            # Textarea normal que funciona con Gradio + editor visual
            component = gr.Textarea(
                label=self.label,
                placeholder=self.placeholder,
                info=self.info,
                lines=self.lines,
                elem_id=self.elem_id,
                elem_classes=["wysiwyg-textarea"]
            )
            
            # Overlay del editor visual
            gr.HTML(f"""
            <div class="wysiwyg-overlay" data-textarea="{self.elem_id}">
                <div 
                    class="wysiwyg-editor" 
                    contenteditable="true" 
                    data-placeholder="{self.placeholder}"
                    id="{self.elem_id}_editor"
                    style="min-height: {self.lines * 1.8}em;"
                ></div>
            </div>
            """, elem_id=f"{self.elem_id}_overlay")
            
        return component
    
    def get_validation_events(self) -> List[Tuple]:
        """No requiere validación especial"""
        return []


class DraggableSectionComponent(UIComponent):
    """Componente de sección arrastrable"""
    
    def __init__(self, section_id: str, title: str, icon: str, content_component: UIComponent):
        super().__init__()
        self.section_id = section_id
        self.title = title
        self.icon = icon
        self.content_component = content_component
    
    def render(self) -> gr.components.Component:
        """Renderiza una sección arrastrable"""
        with gr.Group(elem_classes=["draggable-section"], elem_id=f"section_{self.section_id}"):
            # Header arrastrable
            gr.HTML(f"""
            <div class="section-header draggable-handle" data-section="{self.section_id}">
                <div class="section-title">
                    <span class="drag-icon">⋮⋮</span>
                    <span class="section-icon">{self.icon}</span>
                    <span class="section-text">{self.title}</span>
                </div>
                <button class="collapse-btn" type="button" data-target="section_content_{self.section_id}">
                    <span>▼</span>
                </button>
            </div>
            """)
            
            # Contenido de la sección
            with gr.Column(elem_id=f"section_content_{self.section_id}", elem_classes=["section-content"]):
                content = self.content_component.render()
                
        return content
    
    def get_validation_events(self) -> List[Tuple]:
        """Delega eventos de validación al componente de contenido"""
        return self.content_component.get_validation_events()


class TemplateSelector(UIComponent):
    """Selector de plantillas mejorado"""
    
    def render(self) -> gr.components.Component:
        """Renderiza el selector de plantillas"""
        with gr.Group(elem_classes=["template-selector"]):
            gr.HTML("<h3>🎨 Plantilla de CV</h3>")
            
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
                interactive=True,
                elem_id="template_selector"
            )
            
            # Vista previa mejorada de plantillas
            gr.HTML("""
            <div class="template-preview-grid">
                <div class="template-card modern" data-template="modern">
                    <div class="template-preview">
                        <div class="template-header modern-header"></div>
                        <div class="template-lines">
                            <div class="line long"></div>
                            <div class="line medium"></div>
                            <div class="line short"></div>
                        </div>
                    </div>
                    <div class="template-info">
                        <strong>🎨 Moderna</strong>
                        <small>Limpia y profesional</small>
                    </div>
                </div>
                
                <div class="template-card executive" data-template="executive">
                    <div class="template-preview">
                        <div class="template-header executive-header"></div>
                        <div class="template-lines">
                            <div class="line long"></div>
                            <div class="line medium"></div>
                            <div class="line short"></div>
                        </div>
                    </div>
                    <div class="template-info">
                        <strong>👔 Ejecutiva</strong>
                        <small>Tradicional y formal</small>
                    </div>
                </div>
                
                <div class="template-card creative" data-template="creative">
                    <div class="template-preview">
                        <div class="template-header creative-header"></div>
                        <div class="template-lines">
                            <div class="line long"></div>
                            <div class="line medium"></div>
                            <div class="line short"></div>
                        </div>
                    </div>
                    <div class="template-info">
                        <strong>🌈 Creativa</strong>
                        <small>Vibrante y dinámica</small>
                    </div>
                </div>
                
                <div class="template-card technical" data-template="technical">
                    <div class="template-preview">
                        <div class="template-header technical-header"></div>
                        <div class="template-lines">
                            <div class="line long"></div>
                            <div class="line medium"></div>
                            <div class="line short"></div>
                        </div>
                    </div>
                    <div class="template-info">
                        <strong>💻 Técnica</strong>
                        <small>Estructurada y detallada</small>
                    </div>
                </div>
            </div>
            """)
            
        return template_selector
    
    def get_validation_events(self) -> List[Tuple]:
        """No requiere validación"""
        return []