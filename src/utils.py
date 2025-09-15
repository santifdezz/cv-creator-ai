"""
Utilidades y funciones auxiliares para el generador de CV

Este módulo contiene funciones de validación, formateo y otras utilidades.
"""

from typing import Optional, Dict, Any
from .config import API_CONFIGS
import re

def validate_form_data(nombre: str, email: str, telefono: str, api_provider: str, api_key: Optional[str]) -> Optional[str]:
    """
    Valida los datos del formulario
    
    Args:
        nombre: Nombre completo
        email: Email
        telefono: Teléfono
        api_provider: Proveedor de IA seleccionado
        api_key: API key (opcional según proveedor)
        
    Returns:
        str: Mensaje de error si hay validation error, None si todo está correcto
    """
    
    # Validar campos obligatorios
    if not nombre or not email or not telefono:
        return "❌ Error: Los campos Nombre, Email y Teléfono son obligatorios."
    
    # Validar formato de email
    if not is_valid_email(email):
        return "❌ Error: El formato del email no es válido."
    
    # Validar formato de teléfono
    if not is_valid_phone(telefono):
        return "❌ Error: El formato del teléfono no es válido."
    
    # Validar configuración de API
    if api_provider not in API_CONFIGS:
        return "❌ Error: Proveedor de IA no válido."
    
    # Validar API key según el proveedor
    config = API_CONFIGS[api_provider]
    if config.get("requires_key", False):
        if not api_key or len(api_key.strip()) < 10:
            return f"❌ Error: Se requiere una API key válida para {config['name']}."
    
    return None

def is_valid_email(email: str) -> bool:
    """Valida si el email tiene un formato correcto"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone: str) -> bool:
    """Valida si el teléfono tiene un formato correcto"""
    # Permitir diferentes formatos de teléfono internacionales
    pattern = r'^[\+]?[1-9][\d]{0,15}$|^[\+]?[(]?[\d\s\-\(\)]{8,}$'
    # Limpiar el teléfono de espacios y caracteres especiales para validación
    cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
    return len(cleaned_phone) >= 8 and re.match(pattern, cleaned_phone) is not None

def format_success_message(nombre: str, api_provider: str, modelo: str, ai_content: Dict[str, Any]) -> str:
    """
    Formatea el mensaje de éxito después de generar el CV
    
    Args:
        nombre: Nombre del usuario
        api_provider: Proveedor de IA utilizado
        modelo: Modelo específico usado
        ai_content: Contenido generado por IA
        
    Returns:
        str: Mensaje de éxito formateado
    """
    
    provider_config = API_CONFIGS.get(api_provider, {})
    provider_name = provider_config.get('name', api_provider)
    
    # Determinar el método usado
    if api_provider == "mock":
        method_used = "Plantilla optimizada"
        generation_method = "con plantillas inteligentes"
    else:
        method_used = "IA"
        generation_method = "por inteligencia artificial"
    
    # Truncar resumen para preview
    resumen_preview = ai_content.get('resumen_profesional', '')[:150]
    if len(ai_content.get('resumen_profesional', '')) > 150:
        resumen_preview += '...'
    
    mensaje = f"""
✅ **CV Generado Exitosamente** ({method_used})

**👤 Candidato:** {nombre}
**🤖 Proveedor:** {provider_name}
**🧠 Modelo:** {modelo}

**📝 Resumen Generado:** 
{resumen_preview}

📄 **Tu CV profesional incluye:**
- ✅ Diseño optimizado para ATS (Applicant Tracking Systems)
- ✅ Formato profesional y moderno según estándares 2025
- ✅ Contenido optimizado {generation_method}
- ✅ Estructura clara y legible
- ✅ Categorización inteligente de habilidades
- ✅ Experiencia laboral reformulada con logros

⬇️ **Descarga tu CV usando el botón de abajo**

💡 **Tip:** Revisa el contenido y personalízalo según la oferta específica a la que apliques.
    """
    
    return mensaje

def sanitize_filename(filename: str) -> str:
    """
    Sanitiza un nombre de archivo removiendo caracteres no válidos
    
    Args:
        filename: Nombre de archivo original
        
    Returns:
        str: Nombre de archivo sanitizado
    """
    
    # Remover o reemplazar caracteres no válidos
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    sanitized = re.sub(r'\s+', '_', sanitized)  # Reemplazar espacios con guiones bajos
    
    return sanitized[:100]  # Limitar longitud

def extract_skills_keywords(skills_text: str) -> list:
    """
    Extrae palabras clave de habilidades del texto
    
    Args:
        skills_text: Texto con habilidades separadas por comas
        
    Returns:
        list: Lista de habilidades limpias
    """
    
    if not skills_text:
        return []
    
    # Dividir por comas y limpiar
    skills = [skill.strip() for skill in skills_text.split(',')]
    
    # Filtrar skills vacíos y muy cortos
    skills = [skill for skill in skills if skill and len(skill) > 1]
    
    return skills

def format_phone_number(phone: str) -> str:
    """
    Formatea un número de teléfono para mejor presentación
    
    Args:
        phone: Número de teléfono sin formatear
        
    Returns:
        str: Número de teléfono formateado
    """
    
    # Remover todos los espacios y caracteres especiales
    cleaned = re.sub(r'[^\d\+]', '', phone)
    
    # Si comienza con código de país, mantenerlo
    if cleaned.startswith('+'):
        return cleaned
    elif len(cleaned) == 9:  # Número español típico
        return f"+34 {cleaned}"
    else:
        return phone  # Devolver original si no se puede formatear

def get_provider_status_info(provider_key: str) -> Dict[str, str]:
    """
    Obtiene información de estado del proveedor (gratuito/pago)
    
    Args:
        provider_key: Clave del proveedor
        
    Returns:
        dict: Información del status del proveedor
    """
    
    config = API_CONFIGS.get(provider_key, {})
    is_free = config.get("free", False)
    
    if is_free == True:
        return {
            "status": "🆓 GRATIS",
            "description": "Completamente gratuito",
            "color": "green"
        }
    elif is_free == "Tier gratuito disponible" or is_free == "Créditos gratuitos":
        return {
            "status": "💰 FREEMIUM", 
            "description": "Tier gratuito limitado disponible",
            "color": "orange"
        }
    else:
        return {
            "status": "💳 DE PAGO",
            "description": "Servicio de pago",
            "color": "red"
        }

def estimate_api_cost(provider: str, model: str, prompt_length: int) -> str:
    """
    Estima el costo aproximado de usar una API específica
    
    Args:
        provider: Proveedor de IA
        model: Modelo específico
        prompt_length: Longitud aproximada del prompt
        
    Returns:
        str: Estimación de costo
    """
    
    # Estimaciones aproximadas (pueden variar)
    cost_estimates = {
        "openai": {
            "gpt-3.5-turbo": "~$0.002 por generación",
            "gpt-4": "~$0.03-0.06 por generación",
            "gpt-4-turbo-preview": "~$0.02-0.04 por generación"
        },
        "anthropic": {
            "claude-3-haiku-20240307": "~$0.001-0.003 por generación",
            "claude-3-sonnet-20240229": "~$0.003-0.015 por generación",
            "claude-3-opus-20240229": "~$0.015-0.075 por generación"
        },
        "cohere": {
            "command": "Tier gratuito: 1000 llamadas/mes",
            "command-light": "Tier gratuito: 1000 llamadas/mes"
        }
    }
    
    if provider in cost_estimates and model in cost_estimates[provider]:
        return cost_estimates[provider][model]
    elif provider in ["huggingface_free", "groq", "ollama_local", "mock"]:
        return "Gratuito"
    else:
        return "Consultar documentación del proveedor"

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Trunca texto y añade puntos suspensivos si es necesario
    
    Args:
        text: Texto a truncar
        max_length: Longitud máxima
        
    Returns:
        str: Texto truncado
    """
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."