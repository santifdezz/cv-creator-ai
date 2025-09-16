"""
JavaScript avanzado para componentes interactivos
Incluye WYSIWYG editor, drag-and-drop, y funcionalidades mejoradas
"""

ADVANCED_JAVASCRIPT = """
<script>
    // =============================================================================
    // WYSIWYG EDITOR FUNCTIONALITY
    // =============================================================================
    
    class WYSIWYGEditor {
        constructor(editorId) {
            this.editorId = editorId;
            this.editor = null;
            this.textarea = null;
            this.toolbar = null;
            this.overlay = null;
            this.init();
        }
        
        init() {
            setTimeout(() => {
                this.textarea = document.getElementById(this.editorId);
                this.toolbar = document.querySelector(`[data-target="${this.editorId}"]`);
                this.overlay = document.getElementById(`${this.editorId}_overlay`);
                this.editor = document.getElementById(`${this.editorId}_editor`);
                
                if (this.textarea && this.toolbar && this.editor) {
                    this.setupOverlay();
                    this.setupEvents();
                    this.syncContent();
                }
            }, 1000);
        }
        
        setupOverlay() {
            // Posicionar el overlay sobre el textarea
            if (this.textarea && this.overlay) {
                const textareaRect = this.textarea.getBoundingClientRect();
                const parentRect = this.textarea.parentElement.getBoundingClientRect();
                
                // Ocultar el textarea original pero mantener su funcionalidad
                this.textarea.style.position = 'absolute';
                this.textarea.style.opacity = '0';
                this.textarea.style.pointerEvents = 'none';
                
                // Posicionar el overlay
                this.overlay.style.position = 'relative';
                this.overlay.style.zIndex = '10';
            }
        }
        
        setupEvents() {
            // Toolbar button events
            this.toolbar.addEventListener('click', (e) => {
                if (e.target.classList.contains('toolbar-btn')) {
                    e.preventDefault();
                    const command = e.target.dataset.command;
                    this.executeCommand(command);
                }
            });
            
            // Editor content events
            this.editor.addEventListener('input', () => {
                this.syncToTextarea();
                this.updateToolbarState();
            });
            
            this.editor.addEventListener('keydown', (e) => {
                this.handleKeydown(e);
            });
            
            this.editor.addEventListener('paste', (e) => {
                this.handlePaste(e);
            });
            
            // Sync from textarea to editor (for Gradio integration)
            if (this.textarea) {
                const observer = new MutationObserver(() => {
                    if (this.textarea.value !== this.getMarkdownText()) {
                        this.syncFromTextarea();
                    }
                });
                
                observer.observe(this.textarea, {
                    attributes: true,
                    attributeFilter: ['value']
                });
                
                this.textarea.addEventListener('input', () => {
                    this.syncFromTextarea();
                });
            }
        }
        
        executeCommand(command) {
            this.editor.focus();
            
            switch(command) {
                case 'bold':
                case 'italic':
                case 'underline':
                case 'insertUnorderedList':
                case 'insertOrderedList':
                    document.execCommand(command, false, null);
                    break;
                case 'undo':
                case 'redo':
                    document.execCommand(command, false, null);
                    break;
            }
            
            this.syncToTextarea();
            this.updateToolbarState();
        }
        
        handleKeydown(e) {
            // Handle keyboard shortcuts
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
            
            // Handle Enter key for better list behavior
            if (e.key === 'Enter') {
                const selection = window.getSelection();
                if (selection.rangeCount > 0) {
                    const range = selection.getRangeAt(0);
                    const container = range.commonAncestorContainer;
                    
                    // Check if we're in a list
                    const listItem = container.nodeType === Node.TEXT_NODE 
                        ? container.parentElement.closest('li')
                        : container.closest('li');
                    
                    if (listItem && !listItem.textContent.trim()) {
                        // Exit list if empty item
                        e.preventDefault();
                        document.execCommand('outdent');
                    }
                }
            }
        }
        
        handlePaste(e) {
            e.preventDefault();
            
            // Get plain text from clipboard
            const text = (e.clipboardData || window.clipboardData).getData('text/plain');
            
            // Insert as plain text
            document.execCommand('insertText', false, text);
            
            this.syncToTextarea();
        }
        
        syncToTextarea() {
            if (this.editor && this.textarea) {
                // Convert HTML to markdown-like format for Gradio
                let content = this.editor.innerHTML;
                
                // Convert HTML to markdown-like format
                content = content
                    .replace(/<strong>(.*?)<\\/strong>/g, '**$1**')
                    .replace(/<b>(.*?)<\\/b>/g, '**$1**')
                    .replace(/<em>(.*?)<\\/em>/g, '*$1*')
                    .replace(/<i>(.*?)<\\/i>/g, '*$1*')
                    .replace(/<u>(.*?)<\\/u>/g, '_$1_')
                    .replace(/<ul[^>]*>/g, '')
                    .replace(/<\\/ul>/g, '')
                    .replace(/<ol[^>]*>/g, '')
                    .replace(/<\\/ol>/g, '')
                    .replace(/<li[^>]*>(.*?)<\\/li>/g, '• $1\\n')
                    .replace(/<p[^>]*>(.*?)<\\/p>/g, '$1\\n\\n')
                    .replace(/<div[^>]*>(.*?)<\\/div>/g, '$1\\n')
                    .replace(/<br\\s*\\/?>/g, '\\n')
                    .replace(/&nbsp;/g, ' ')
                    .replace(/&amp;/g, '&')
                    .replace(/&lt;/g, '<')
                    .replace(/&gt;/g, '>')
                    .replace(/\\n\\s*\\n\\s*\\n/g, '\\n\\n') // Remove excessive line breaks
                    .trim();
                
                this.textarea.value = content;
                
                // Trigger Gradio update
                this.textarea.dispatchEvent(new Event('input', { bubbles: true }));
                this.textarea.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }
        
        syncFromTextarea() {
            if (this.editor && this.textarea && this.textarea.value !== this.getMarkdownText()) {
                // Convert markdown-like format back to HTML
                let content = this.textarea.value;
                
                if (content) {
                    content = content
                        .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
                        .replace(/\\*(.*?)\\*/g, '<em>$1</em>')
                        .replace(/_(.*?)_/g, '<u>$1</u>')
                        .replace(/^• (.*)$/gm, '<li>$1</li>')
                        .replace(/((?:<li>.*<\\/li>\\s*)+)/g, '<ul>$1</ul>')
                        .replace(/\\n\\n/g, '</p><p>')
                        .replace(/\\n/g, '<br>')
                        .replace(/^(.)/gm, '<p>$1')
                        .replace(/(.)$/gm, '$1</p>')
                        .replace(/<p><\\/p>/g, '')
                        .replace(/<p>(<ul>.*<\\/ul>)<\\/p>/g, '$1')
                        .replace(/<p>(<li>.*<\\/li>)<\\/p>/g, '$1');
                    
                    this.editor.innerHTML = content;
                } else {
                    this.editor.innerHTML = '';
                }
            }
        }
        
        syncContent() {
            // Initial sync
            if (this.textarea && this.textarea.value) {
                this.syncFromTextarea();
            }
        }
        
        updateToolbarState() {
            if (!this.toolbar) return;
            
            const buttons = this.toolbar.querySelectorAll('.toolbar-btn');
            buttons.forEach(btn => {
                const command = btn.dataset.command;
                
                try {
                    if (['bold', 'italic', 'underline'].includes(command)) {
                        const isActive = document.queryCommandState(command);
                        btn.classList.toggle('active', isActive);
                    }
                } catch (e) {
                    // Command might not be supported
                }
            });
        }
        
        getMarkdownText() {
            if (!this.editor) return '';
            
            let content = this.editor.innerHTML;
            return content
                .replace(/<strong>(.*?)<\\/strong>/g, '**$1**')
                .replace(/<b>(.*?)<\\/b>/g, '**$1**')
                .replace(/<em>(.*?)<\\/em>/g, '*$1*')
                .replace(/<i>(.*?)<\\/i>/g, '*$1*')
                .replace(/<u>(.*?)<\\/u>/g, '_$1_')
                .replace(/<[^>]*>/g, '')
                .replace(/&nbsp;/g, ' ')
                .trim();
        }
    }
    
    // =============================================================================
    // DRAG AND DROP FUNCTIONALITY
    // =============================================================================
    
    class DragDropManager {
        constructor() {
            this.draggedElement = null;
            this.placeholder = null;
            this.sections = [];
            this.init();
        }
        
        init() {
            setTimeout(() => {
                this.setupDragAndDrop();
                this.setupCollapsible();
            }, 1000);
        }
        
        setupDragAndDrop() {
            const sections = document.querySelectorAll('.draggable-section');
            
            sections.forEach(section => {
                const handle = section.querySelector('.draggable-handle');
                if (handle) {
                    handle.draggable = true;
                    
                    handle.addEventListener('dragstart', (e) => {
                        this.handleDragStart(e, section);
                    });
                    
                    section.addEventListener('dragover', (e) => {
                        this.handleDragOver(e);
                    });
                    
                    section.addEventListener('drop', (e) => {
                        this.handleDrop(e, section);
                    });
                    
                    section.addEventListener('dragenter', (e) => {
                        this.handleDragEnter(e, section);
                    });
                    
                    section.addEventListener('dragleave', (e) => {
                        this.handleDragLeave(e, section);
                    });
                }
            });
            
            document.addEventListener('dragend', () => {
                this.handleDragEnd();
            });
        }
        
        handleDragStart(e, section) {
            this.draggedElement = section;
            section.classList.add('dragging');
            
            // Create placeholder
            this.placeholder = this.createPlaceholder();
            
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/html', section.outerHTML);
            
            // Add visual feedback
            setTimeout(() => {
                section.style.display = 'none';
            }, 0);
        }
        
        handleDragOver(e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
        }
        
        handleDragEnter(e, section) {
            if (section !== this.draggedElement) {
                section.classList.add('drag-over');
                
                // Show placeholder
                if (this.placeholder && !this.placeholder.classList.contains('active')) {
                    this.placeholder.classList.add('active');
                    section.parentNode.insertBefore(this.placeholder, section);
                }
            }
        }
        
        handleDragLeave(e, section) {
            // Only remove if actually leaving the section
            const rect = section.getBoundingClientRect();
            const x = e.clientX;
            const y = e.clientY;
            
            if (x < rect.left || x > rect.right || y < rect.top || y > rect.bottom) {
                section.classList.remove('drag-over');
            }
        }
        
        handleDrop(e, section) {
            e.preventDefault();
            
            if (section !== this.draggedElement) {
                // Insert dragged element before the target
                section.parentNode.insertBefore(this.draggedElement, section);
                
                // Show success feedback
                this.showNotification('✅ Sección reordenada correctamente', 'success');
                
                // Update section order data
                this.updateSectionOrder();
            }
            
            section.classList.remove('drag-over');
        }
        
        handleDragEnd() {
            if (this.draggedElement) {
                this.draggedElement.classList.remove('dragging');
                this.draggedElement.style.display = '';
                this.draggedElement = null;
            }
            
            if (this.placeholder) {
                this.placeholder.remove();
                this.placeholder = null;
            }
            
            // Remove all drag-over classes
            document.querySelectorAll('.drag-over').forEach(el => {
                el.classList.remove('drag-over');
            });
        }
        
        createPlaceholder() {
            const placeholder = document.createElement('div');
            placeholder.className = 'drag-placeholder';
            placeholder.innerHTML = '↕️ Suelta aquí para reordenar';
            return placeholder;
        }
        
        updateSectionOrder() {
            const sections = document.querySelectorAll('.draggable-section');
            const order = Array.from(sections).map(section => {
                return section.id || section.querySelector('[data-section]')?.dataset.section;
            }).filter(Boolean);
            
            // Store order in localStorage
            localStorage.setItem('cv_section_order', JSON.stringify(order));
            
            console.log('📋 Section order updated:', order);
        }
        
        setupCollapsible() {
            document.addEventListener('click', (e) => {
                if (e.target.closest('.collapse-btn')) {
                    const btn = e.target.closest('.collapse-btn');
                    const targetId = btn.dataset.target;
                    const target = document.getElementById(targetId);
                    
                    if (target) {
                        const isCollapsed = target.classList.contains('collapsed');
                        
                        if (isCollapsed) {
                            target.classList.remove('collapsed');
                            btn.classList.remove('collapsed');
                        } else {
                            target.classList.add('collapsed');
                            btn.classList.add('collapsed');
                        }
                        
                        // Save collapsed state
                        const collapsedSections = JSON.parse(localStorage.getItem('cv_collapsed_sections') || '[]');
                        
                        if (isCollapsed) {
                            const index = collapsedSections.indexOf(targetId);
                            if (index > -1) collapsedSections.splice(index, 1);
                        } else {
                            if (!collapsedSections.includes(targetId)) {
                                collapsedSections.push(targetId);
                            }
                        }
                        
                        localStorage.setItem('cv_collapsed_sections', JSON.stringify(collapsedSections));
                    }
                }
            });
            
            // Restore collapsed state
            setTimeout(() => {
                const collapsedSections = JSON.parse(localStorage.getItem('cv_collapsed_sections') || '[]');
                collapsedSections.forEach(sectionId => {
                    const section = document.getElementById(sectionId);
                    const btn = document.querySelector(`[data-target="${sectionId}"]`);
                    
                    if (section && btn) {
                        section.classList.add('collapsed');
                        btn.classList.add('collapsed');
                    }
                });
            }, 1500);
        }
        
        showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `notification notification-${type}`;
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
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
            
            setTimeout(() => {
                notification.style.opacity = '1';
                notification.style.transform = 'translateX(0)';
            }, 10);
            
            setTimeout(() => {
                notification.style.opacity = '0';
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }
    }
    
    // =============================================================================
    // TEMPLATE SELECTOR ENHANCEMENT
    // =============================================================================
    
    class TemplateSelector {
        constructor() {
            this.init();
        }
        
        init() {
            setTimeout(() => {
                this.setupTemplateCards();
            }, 1000);
        }
        
        setupTemplateCards() {
            const cards = document.querySelectorAll('.template-card');
            const dropdown = document.getElementById('template_selector');
            
            cards.forEach(card => {
                card.addEventListener('click', () => {
                    const template = card.dataset.template;
                    
                    if (template && dropdown) {
                        // Update dropdown value
                        dropdown.value = template;
                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                        
                        // Update visual selection
                        cards.forEach(c => c.classList.remove('selected'));
                        card.classList.add('selected');
                        
                        // Show feedback
                        this.showTemplateSelected(template);
                    }
                });
            });
            
            // Sync with dropdown changes
            if (dropdown) {
                dropdown.addEventListener('change', () => {
                    const selectedTemplate = dropdown.value;
                    cards.forEach(card => {
                        card.classList.toggle('selected', card.dataset.template === selectedTemplate);
                    });
                });
                
                // Set initial selection
                const initialTemplate = dropdown.value;
                cards.forEach(card => {
                    card.classList.toggle('selected', card.dataset.template === initialTemplate);
                });
            }
        }
        
        showTemplateSelected(template) {
            const templateNames = {
                'modern': '🎨 Moderna',
                'executive': '👔 Ejecutiva', 
                'creative': '🌈 Creativa',
                'technical': '💻 Técnica'
            };
            
            const name = templateNames[template] || template;
            this.showNotification(`Plantilla ${name} seleccionada`, 'success');
        }
        
        showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `notification notification-${type}`;
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: ${type === 'success' ? '#10b981' : '#3b82f6'};
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
            
            setTimeout(() => {
                notification.style.opacity = '1';
                notification.style.transform = 'translateX(0)';
            }, 10);
            
            setTimeout(() => {
                notification.style.opacity = '0';
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }
    }
    
    // =============================================================================
    // INITIALIZATION
    // =============================================================================
    
    document.addEventListener('DOMContentLoaded', function() {
        console.log('🚀 Initializing advanced CV editor components...');
        
        // Initialize components with delays to ensure DOM is ready
        setTimeout(() => {
            // Initialize WYSIWYG editors
            const editors = ['experiencia', 'formacion', 'habilidades', 'resumen_profesional'];
            editors.forEach(editorId => {
                new WYSIWYGEditor(editorId);
            });
            
            // Initialize drag and drop
            new DragDropManager();
            
            // Initialize template selector
            new TemplateSelector();
            
            console.log('✅ Advanced components initialized');
        }, 2000);
    });
    
    // Also initialize if DOM is already ready
    if (document.readyState !== 'loading') {
        setTimeout(() => {
            const event = new Event('DOMContentLoaded');
            document.dispatchEvent(event);
        }, 1000);
    }
</script>
"""