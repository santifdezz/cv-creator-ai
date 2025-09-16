"""
Estilos CSS para componentes avanzados del CVisionAI
Incluye estilos para WYSIWYG, drag-and-drop, y componentes modulares
"""

ADVANCED_CSS = """
<style>
    /* Variables CSS extendidas */
    :root {
        --primary-color: #2563eb;
        --primary-hover: #1d4ed8;
        --secondary-color: #64748b;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --background-color: #f8fafc;
        --surface-color: #ffffff;
        --border-color: #e2e8f0;
        --border-hover: #cbd5e1;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --text-muted: #94a3b8;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --border-radius: 8px;
        --border-radius-lg: 12px;
        --transition: all 0.3s ease;
    }

    /* =============================================================================
       WYSIWYG EDITOR STYLES
    ============================================================================= */
    
    .wysiwyg-textarea {
        position: relative !important;
    }
    
    .wysiwyg-overlay {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        z-index: 10 !important;
        pointer-events: none !important;
    }
    
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
        pointer-events: all;
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
        border: 1px solid var(--border-color);
        border-radius: 0 0 var(--border-radius) var(--border-radius);
        overflow: hidden;
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
        pointer-events: all;
        position: relative;
        z-index: 15;
        margin-top: -1px; /* Overlap with toolbar */
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
    
    /* Hide the original textarea when WYSIWYG is active */
    .wysiwyg-textarea textarea {
        opacity: 0 !important;
        position: absolute !important;
        pointer-events: none !important;
        z-index: 1 !important;
    }

    /* =============================================================================
       DRAG AND DROP STYLES
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

    /* =============================================================================
       TEMPLATE SELECTOR ENHANCED
    ============================================================================= */
    
    .template-preview-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-top: 16px;
        padding: 16px;
        background: var(--background-color);
        border-radius: var(--border-radius);
    }
    
    .template-card {
        background: var(--surface-color);
        border: 2px solid var(--border-color);
        border-radius: var(--border-radius-lg);
        padding: 16px;
        cursor: pointer;
        transition: var(--transition);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .template-card:hover {
        border-color: var(--primary-color);
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }
    
    .template-card.selected {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    .template-preview {
        width: 100%;
        height: 120px;
        border: 1px solid var(--border-color);
        border-radius: 6px;
        margin-bottom: 12px;
        position: relative;
        overflow: hidden;
        background: white;
    }
    
    .template-header {
        height: 30px;
        width: 100%;
    }
    
    .modern-header {
        background: linear-gradient(135deg, var(--primary-color), #3b82f6);
    }
    
    .executive-header {
        background: linear-gradient(135deg, #374151, #4b5563);
    }
    
    .creative-header {
        background: linear-gradient(135deg, #7c3aed, #a855f7);
    }
    
    .technical-header {
        background: linear-gradient(135deg, #059669, #10b981);
    }
    
    .template-lines {
        padding: 12px 8px;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    
    .line {
        height: 4px;
        background: var(--border-color);
        border-radius: 2px;
    }
    
    .line.long {
        width: 90%;
    }
    
    .line.medium {
        width: 70%;
    }
    
    .line.short {
        width: 50%;
    }
    
    .template-info strong {
        display: block;
        color: var(--text-primary);
        font-size: 14px;
        margin-bottom: 4px;
    }
    
    .template-info small {
        color: var(--text-secondary);
        font-size: 12px;
    }

    /* =============================================================================
       ENHANCED FORM COMPONENTS
    ============================================================================= */
    
    .group {
        background: var(--surface-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--border-radius-lg) !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: var(--shadow-sm) !important;
        transition: var(--transition) !important;
        position: relative !important;
    }
    
    .group:hover {
        box-shadow: var(--shadow-md) !important;
        border-color: var(--border-hover) !important;
    }
    
    .group h3 {
        margin: 0 0 20px 0 !important;
        color: var(--text-primary) !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }
    
    /* Enhanced input styling */
    .gr-textbox,
    .gr-dropdown,
    .gr-textarea {
        border: 1px solid var(--border-color) !important;
        border-radius: var(--border-radius) !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        transition: var(--transition) !important;
        background: var(--surface-color) !important;
        color: var(--text-primary) !important;
    }
    
    .gr-textbox:focus,
    .gr-dropdown:focus,
    .gr-textarea:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        outline: none !important;
    }
    
    .gr-textbox:hover,
    .gr-dropdown:hover,
    .gr-textarea:hover {
        border-color: var(--border-hover) !important;
    }
    
    /* Validation feedback styling */
    .validation-feedback {
        margin-top: 6px !important;
        font-size: 12px !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
        font-weight: 500 !important;
    }
    
    .validation-feedback.success {
        color: var(--success-color) !important;
    }
    
    .validation-feedback.error {
        color: var(--error-color) !important;
    }

    /* =============================================================================
       RESPONSIVE DESIGN FOR NEW COMPONENTS
    ============================================================================= */
    
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
        
        .template-preview-grid {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 12px;
            padding: 12px;
        }
        
        .template-card {
            padding: 12px;
        }
        
        .template-preview {
            height: 80px;
            margin-bottom: 8px;
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
    
    @media (max-width: 480px) {
        .wysiwyg-toolbar {
            flex-wrap: wrap;
            padding: 4px 6px;
        }
        
        .toolbar-group {
            margin-bottom: 4px;
        }
        
        .template-preview-grid {
            grid-template-columns: 1fr;
            gap: 8px;
            padding: 8px;
        }
        
        .section-content {
            padding: 16px !important;
        }
    }

    /* =============================================================================
       LOADING AND ANIMATION ENHANCEMENTS
    ============================================================================= */
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.5s ease forwards;
    }
    
    .slide-in {
        animation: slideIn 0.4s ease forwards;
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* Success/Error states */
    .success-state {
        border-color: var(--success-color) !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
    }
    
    .error-state {
        border-color: var(--error-color) !important;
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1) !important;
    }
    
    /* Accessibility improvements */
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }
    
    /* Focus indicators for keyboard navigation */
    .toolbar-btn:focus,
    .template-card:focus,
    .collapse-btn:focus {
        outline: 2px solid var(--primary-color);
        outline-offset: 2px;
    }
    
    /* High contrast mode support */
    @media (prefers-contrast: high) {
        :root {
            --border-color: #000000;
            --text-primary: #000000;
            --text-secondary: #333333;
        }
    }
    
    /* Reduced motion for accessibility */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
</style>
"""