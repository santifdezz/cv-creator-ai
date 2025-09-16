"""
Componente WYSIWYG con Editor de Texto Rico y Drag-and-Drop - CV Creator AI
Integra funcionalidades avanzadas de edición y reorganización visual
"""

import gradio as gr
from typing import Dict, List, Any


class WYSIWYGComponent:
    """Componente WYSIWYG con editor rico y drag-and-drop"""
    
    def __init__(self):
        self.components = {}
    
    def render(self) -> Dict[str, Any]:
        """Renderizar el componente WYSIWYG"""
        
        with gr.Group():
            gr.Markdown("### ✨ **Editor Avanzado de CV**")
            gr.Markdown("*Edita tu CV con herramientas profesionales de formato y reorganización*")
            
            # Editor WYSIWYG principal
            self.components['wysiwyg_editor'] = gr.HTML(
                value=self._get_wysiwyg_editor_html(),
                elem_id="wysiwyg_editor_container"
            )
            
            # Zona de drag-and-drop para secciones
            self.components['draggable_sections'] = gr.HTML(
                value=self._get_draggable_sections_html(),
                elem_id="draggable_sections_container"
            )
            
            # Controles de formato
            with gr.Row():
                self.components['bold_btn'] = gr.Button("📝 Negrita", size="sm", variant="secondary")
                self.components['italic_btn'] = gr.Button("📖 Cursiva", size="sm", variant="secondary")
                self.components['list_btn'] = gr.Button("📋 Lista", size="sm", variant="secondary")
                self.components['link_btn'] = gr.Button("🔗 Enlace", size="sm", variant="secondary")
            
            # Preview del contenido formateado
            self.components['formatted_preview'] = gr.HTML(
                value="<div id='content_preview'>Vista previa aparecerá aquí...</div>",
                label="Vista Previa Formateada"
            )
        
        return self.components
    
    def _get_wysiwyg_editor_html(self) -> str:
        """HTML para el editor WYSIWYG"""
        return """
        <div id="wysiwyg-container" style="border: 2px solid #e5e7eb; border-radius: 8px; background: white;">
            <!-- Toolbar del editor -->
            <div id="wysiwyg-toolbar" style="border-bottom: 1px solid #e5e7eb; padding: 8px; background: #f9fafb; display: flex; gap: 4px; flex-wrap: wrap;">
                <button class="toolbar-btn" data-command="bold" title="Negrita">
                    <strong>B</strong>
                </button>
                <button class="toolbar-btn" data-command="italic" title="Cursiva">
                    <em>I</em>
                </button>
                <button class="toolbar-btn" data-command="underline" title="Subrayado">
                    <u>U</u>
                </button>
                <div class="toolbar-separator"></div>
                <button class="toolbar-btn" data-command="insertUnorderedList" title="Lista con viñetas">
                    • Lista
                </button>
                <button class="toolbar-btn" data-command="insertOrderedList" title="Lista numerada">
                    1. Lista
                </button>
                <div class="toolbar-separator"></div>
                <button class="toolbar-btn" data-command="justifyLeft" title="Alinear izquierda">
                    ←
                </button>
                <button class="toolbar-btn" data-command="justifyCenter" title="Centrar">
                    ↔
                </button>
                <button class="toolbar-btn" data-command="justifyRight" title="Alinear derecha">
                    →
                </button>
                <div class="toolbar-separator"></div>
                <select class="toolbar-select" onchange="document.execCommand('fontSize', false, this.value)">
                    <option value="2">Pequeño</option>
                    <option value="3" selected>Normal</option>
                    <option value="4">Grande</option>
                    <option value="5">Muy Grande</option>
                </select>
            </div>
            
            <!-- Área de edición -->
            <div id="wysiwyg-editor" 
                 contenteditable="true" 
                 style="min-height: 300px; padding: 16px; outline: none; line-height: 1.6;"
                 data-placeholder="Escribe aquí el contenido de tu CV. Usa la barra de herramientas para dar formato...">
                
                <h3>👤 Información Personal</h3>
                <p><strong>Nombre:</strong> [Tu nombre aquí]</p>
                <p><strong>Email:</strong> [tu.email@ejemplo.com]</p>
                <p><strong>Teléfono:</strong> [+34 XXX XXX XXX]</p>
                
                <h3>🎯 Objetivo Profesional</h3>
                <p>[Describe tu objetivo profesional aquí...]</p>
                
                <h3>💼 Experiencia Laboral</h3>
                <ul>
                    <li><strong>Puesto - Empresa (Fechas)</strong>
                        <ul>
                            <li>Responsabilidad 1</li>
                            <li>Responsabilidad 2</li>
                            <li>Logro destacado</li>
                        </ul>
                    </li>
                </ul>
                
                <h3>🎓 Educación</h3>
                <ul>
                    <li><strong>Título - Institución (Año)</strong></li>
                </ul>
                
                <h3>🛠️ Habilidades</h3>
                <ul>
                    <li>Habilidad técnica 1</li>
                    <li>Habilidad técnica 2</li>
                    <li>Habilidad técnica 3</li>
                </ul>
            </div>
        </div>
        
        <style>
        .toolbar-btn {
            padding: 6px 10px;
            border: 1px solid #d1d5db;
            background: white;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.2s;
        }
        
        .toolbar-btn:hover {
            background: #f3f4f6;
            border-color: #9ca3af;
        }
        
        .toolbar-btn.active {
            background: #3b82f6;
            color: white;
            border-color: #2563eb;
        }
        
        .toolbar-separator {
            width: 1px;
            height: 24px;
            background: #d1d5db;
            margin: 0 4px;
        }
        
        .toolbar-select {
            padding: 4px 8px;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            background: white;
            font-size: 12px;
        }
        
        #wysiwyg-editor:empty:before {
            content: attr(data-placeholder);
            color: #9ca3af;
            font-style: italic;
        }
        
        #wysiwyg-editor:focus {
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
        }
        
        #wysiwyg-editor h3 {
            color: #374151;
            margin-top: 24px;
            margin-bottom: 12px;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 4px;
        }
        
        #wysiwyg-editor ul {
            margin-left: 20px;
        }
        
        #wysiwyg-editor li {
            margin-bottom: 4px;
        }
        </style>
        
        <script>
        // Inicializar el editor WYSIWYG
        document.addEventListener('DOMContentLoaded', function() {
            const toolbar = document.getElementById('wysiwyg-toolbar');
            const editor = document.getElementById('wysiwyg-editor');
            
            // Manejar clics en la toolbar
            toolbar.addEventListener('click', function(e) {
                if (e.target.classList.contains('toolbar-btn')) {
                    e.preventDefault();
                    const command = e.target.dataset.command;
                    document.execCommand(command, false, null);
                    
                    // Actualizar estado visual del botón
                    updateToolbarState();
                }
            });
            
            // Actualizar estado de la toolbar
            function updateToolbarState() {
                const buttons = toolbar.querySelectorAll('.toolbar-btn');
                buttons.forEach(btn => {
                    const command = btn.dataset.command;
                    if (document.queryCommandState(command)) {
                        btn.classList.add('active');
                    } else {
                        btn.classList.remove('active');
                    }
                });
            }
            
            // Escuchar cambios en el editor
            editor.addEventListener('keyup', updateToolbarState);
            editor.addEventListener('mouseup', updateToolbarState);
        });
        </script>
        """
    
    def _get_draggable_sections_html(self) -> str:
        """HTML para las secciones arrastrables"""
        return """
        <div id="draggable-sections" style="margin-top: 20px;">
            <h4 style="margin-bottom: 12px; color: #374151;">📋 Reorganiza las secciones de tu CV</h4>
            <div id="sections-container" style="display: flex; flex-direction: column; gap: 8px;">
                
                <div class="draggable-section" data-section="personal" style="order: 1;">
                    <div class="section-header">
                        <span class="drag-handle">⋮⋮</span>
                        <span class="section-title">👤 Información Personal</span>
                        <span class="section-toggle">👁️</span>
                    </div>
                </div>
                
                <div class="draggable-section" data-section="objetivo" style="order: 2;">
                    <div class="section-header">
                        <span class="drag-handle">⋮⋮</span>
                        <span class="section-title">🎯 Objetivo Profesional</span>
                        <span class="section-toggle">👁️</span>
                    </div>
                </div>
                
                <div class="draggable-section" data-section="experiencia" style="order: 3;">
                    <div class="section-header">
                        <span class="drag-handle">⋮⋮</span>
                        <span class="section-title">💼 Experiencia Laboral</span>
                        <span class="section-toggle">👁️</span>
                    </div>
                </div>
                
                <div class="draggable-section" data-section="educacion" style="order: 4;">
                    <div class="section-header">
                        <span class="drag-handle">⋮⋮</span>
                        <span class="section-title">🎓 Educación</span>
                        <span class="section-toggle">👁️</span>
                    </div>
                </div>
                
                <div class="draggable-section" data-section="habilidades" style="order: 5;">
                    <div class="section-header">
                        <span class="drag-handle">⋮⋮</span>
                        <span class="section-title">🛠️ Habilidades</span>
                        <span class="section-toggle">👁️</span>
                    </div>
                </div>
                
                <div class="draggable-section" data-section="idiomas" style="order: 6;">
                    <div class="section-header">
                        <span class="drag-handle">⋮⋮</span>
                        <span class="section-title">🌍 Idiomas</span>
                        <span class="section-toggle">👁️</span>
                    </div>
                </div>
                
            </div>
        </div>
        
        <style>
        .draggable-section {
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            padding: 12px;
            cursor: move;
            transition: all 0.3s ease;
            user-select: none;
        }
        
        .draggable-section:hover {
            border-color: #3b82f6;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }
        
        .draggable-section.dragging {
            opacity: 0.6;
            transform: rotate(2deg);
            z-index: 1000;
        }
        
        .section-header {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .drag-handle {
            color: #9ca3af;
            font-size: 16px;
            cursor: grab;
        }
        
        .drag-handle:active {
            cursor: grabbing;
        }
        
        .section-title {
            flex: 1;
            font-weight: 600;
            color: #374151;
        }
        
        .section-toggle {
            cursor: pointer;
            font-size: 14px;
            opacity: 0.7;
            transition: opacity 0.2s;
        }
        
        .section-toggle:hover {
            opacity: 1;
        }
        
        .drop-indicator {
            height: 4px;
            background: #3b82f6;
            border-radius: 2px;
            margin: 4px 0;
            opacity: 0;
            transition: opacity 0.2s;
        }
        
        .drop-indicator.active {
            opacity: 1;
        }
        </style>
        
        <script>
        // Funcionalidad de drag-and-drop
        document.addEventListener('DOMContentLoaded', function() {
            const container = document.getElementById('sections-container');
            let draggedElement = null;
            let dropIndicators = [];
            
            // Crear indicadores de drop
            function createDropIndicators() {
                const sections = container.querySelectorAll('.draggable-section');
                dropIndicators.forEach(indicator => indicator.remove());
                dropIndicators = [];
                
                sections.forEach((section, index) => {
                    const indicator = document.createElement('div');
                    indicator.className = 'drop-indicator';
                    container.insertBefore(indicator, section);
                    dropIndicators.push(indicator);
                });
                
                // Indicador final
                const finalIndicator = document.createElement('div');
                finalIndicator.className = 'drop-indicator';
                container.appendChild(finalIndicator);
                dropIndicators.push(finalIndicator);
            }
            
            // Eventos de drag
            container.addEventListener('dragstart', function(e) {
                if (e.target.classList.contains('draggable-section')) {
                    draggedElement = e.target;
                    e.target.classList.add('dragging');
                    createDropIndicators();
                }
            });
            
            container.addEventListener('dragend', function(e) {
                if (e.target.classList.contains('draggable-section')) {
                    e.target.classList.remove('dragging');
                    draggedElement = null;
                    dropIndicators.forEach(indicator => {
                        indicator.classList.remove('active');
                        indicator.remove();
                    });
                    dropIndicators = [];
                    
                    // Actualizar orden en el editor WYSIWYG
                    updateEditorSectionOrder();
                }
            });
            
            container.addEventListener('dragover', function(e) {
                e.preventDefault();
                
                if (draggedElement) {
                    const afterElement = getDragAfterElement(container, e.clientY);
                    dropIndicators.forEach(indicator => indicator.classList.remove('active'));
                    
                    if (afterElement == null) {
                        const lastIndicator = dropIndicators[dropIndicators.length - 1];
                        if (lastIndicator) lastIndicator.classList.add('active');
                    } else {
                        const index = Array.from(container.children).indexOf(afterElement);
                        const indicatorIndex = Math.floor(index / 2);
                        if (dropIndicators[indicatorIndex]) {
                            dropIndicators[indicatorIndex].classList.add('active');
                        }
                    }
                }
            });
            
            container.addEventListener('drop', function(e) {
                e.preventDefault();
                
                if (draggedElement) {
                    const afterElement = getDragAfterElement(container, e.clientY);
                    
                    if (afterElement == null) {
                        container.appendChild(draggedElement);
                    } else {
                        container.insertBefore(draggedElement, afterElement);
                    }
                }
            });
            
            // Función auxiliar para determinar posición de drop
            function getDragAfterElement(container, y) {
                const draggableElements = [...container.querySelectorAll('.draggable-section:not(.dragging)')];
                
                return draggableElements.reduce((closest, child) => {
                    const box = child.getBoundingClientRect();
                    const offset = y - box.top - box.height / 2;
                    
                    if (offset < 0 && offset > closest.offset) {
                        return { offset: offset, element: child };
                    } else {
                        return closest;
                    }
                }, { offset: Number.NEGATIVE_INFINITY }).element;
            }
            
            // Actualizar orden en el editor WYSIWYG
            function updateEditorSectionOrder() {
                const sections = container.querySelectorAll('.draggable-section');
                const sectionOrder = Array.from(sections).map(section => section.dataset.section);
                
                console.log('Nuevo orden de secciones:', sectionOrder);
                // Aquí puedes implementar la lógica para reordenar el contenido del editor
            }
            
            // Hacer elementos arrastrables
            const sections = container.querySelectorAll('.draggable-section');
            sections.forEach(section => {
                section.draggable = true;
            });
        });
        </script>
        """
    
    def get_inputs(self) -> List[Any]:
        """Retornar lista de inputs del componente"""
        return [self.components.get('wysiwyg_editor', None)]
    
    def get_editor_content(self) -> str:
        """Obtener contenido del editor WYSIWYG"""
        # Esta función se ejecutaría con JavaScript para obtener el contenido
        return ""