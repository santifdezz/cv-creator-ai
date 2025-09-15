"""
Configuración de APIs y modelos disponibles para el generador de CV

Este módulo contiene todas las configuraciones de los diferentes proveedores
de IA disponibles, incluyendo modelos, endpoints y características.
"""

import os
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()  # Cargar variables de .env si existe
except ImportError:
    pass  # dotenv es opcional

# Configuración de APIs disponibles
API_CONFIGS = {
    "huggingface_free": {
        "name": "🤗 Hugging Face (Gratis)",
        "models": {
            "microsoft/DialoGPT-large": "DialoGPT Large",
            "microsoft/DialoGPT-medium": "DialoGPT Medium", 
            "facebook/blenderbot-400M-distill": "BlenderBot 400M",
            "google/flan-t5-large": "FLAN-T5 Large",
            "google/flan-t5-base": "FLAN-T5 Base",
            "bigscience/bloom-560m": "BLOOM 560M",
            "gpt2": "GPT-2"
        },
        "endpoint": "https://api-inference.huggingface.co/models/",
        "requires_key": True,
        "free": True,
        "description": "Modelos gratuitos de Hugging Face con límites de uso",
        "docs_url": "https://huggingface.co/docs/api-inference/index"
    },
    "openai": {
        "name": "🤖 OpenAI",
        "models": {
            "gpt-3.5-turbo": "GPT-3.5 Turbo",
            "gpt-3.5-turbo-1106": "GPT-3.5 Turbo (Nov 2023)",
            "gpt-4": "GPT-4",
            "gpt-4-turbo-preview": "GPT-4 Turbo",
            "gpt-4-1106-preview": "GPT-4 Turbo (Nov 2023)"
        },
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "requires_key": True,
        "free": False,
        "description": "Modelos de OpenAI con excelente calidad (de pago)",
        "docs_url": "https://platform.openai.com/docs/api-reference"
    },
    "anthropic": {
        "name": "🧠 Anthropic Claude",
        "models": {
            "claude-3-haiku-20240307": "Claude 3 Haiku",
            "claude-3-sonnet-20240229": "Claude 3 Sonnet", 
            "claude-3-opus-20240229": "Claude 3 Opus",
            "claude-3-5-sonnet-20241022": "Claude 3.5 Sonnet"
        },
        "endpoint": "https://api.anthropic.com/v1/messages",
        "requires_key": True,
        "free": False,
        "description": "Claude de Anthropic, excelente para escritura (de pago)",
        "docs_url": "https://docs.anthropic.com/claude/reference"
    },
    "cohere": {
        "name": "🚀 Cohere",
        "models": {
            "command": "Command",
            "command-light": "Command Light",
            "command-nightly": "Command Nightly",
            "command-r": "Command R",
            "command-r-plus": "Command R+"
        },
        "endpoint": "https://api.cohere.ai/v1/generate",
        "requires_key": True,
        "free": "Tier gratuito disponible",
        "description": "Cohere con tier gratuito mensual",
        "docs_url": "https://docs.cohere.com/reference/generate"
    },
    "groq": {
        "name": "⚡ Groq (Rápido y Gratuito)",
        "models": {
            "llama2-70b-4096": "Llama 2 70B",
            "mixtral-8x7b-32768": "Mixtral 8x7B",
            "gemma-7b-it": "Gemma 7B"
        },
        "endpoint": "https://api.groq.com/openai/v1/chat/completions",
        "requires_key": True,
        "free": True,
        "description": "Groq - Inferencia súper rápida con modelos gratuitos",
        "docs_url": "https://console.groq.com/docs/quickstart"
    },
    "ollama_local": {
        "name": "🏠 Ollama Local",
        "models": {
            "llama2": "Llama 2 7B",
            "llama2:13b": "Llama 2 13B",
            "codellama": "Code Llama 7B", 
            "codellama:13b": "Code Llama 13B",
            "mistral": "Mistral 7B",
            "neural-chat": "Neural Chat 7B",
            "orca-mini": "Orca Mini 3B",
            "phi": "Microsoft Phi-2"
        },
        "endpoint": "http://localhost:11434/api/generate",
        "requires_key": False,
        "free": True,
        "description": "Modelos locales con Ollama (requiere instalación)",
        "docs_url": "https://ollama.ai/docs"
    },
    "together": {
        "name": "🤝 Together AI",
        "models": {
            "togethercomputer/llama-2-7b-chat": "Llama 2 7B Chat",
            "togethercomputer/llama-2-13b-chat": "Llama 2 13B Chat",
            "mistralai/Mistral-7B-Instruct-v0.1": "Mistral 7B Instruct",
            "NousResearch/Nous-Hermes-2-Yi-34B": "Nous Hermes 2"
        },
        "endpoint": "https://api.together.xyz/inference",
        "requires_key": True,
        "free": "Créditos gratuitos",
        "description": "Together AI con créditos gratuitos iniciales",
        "docs_url": "https://docs.together.ai/"
    },
    "mock": {
        "name": "🎭 Simulado (Sin API)",
        "models": {
            "mock-basic": "Plantilla Básica",
            "mock-professional": "Plantilla Profesional", 
            "mock-creative": "Plantilla Creativa"
        },
        "endpoint": None,
        "requires_key": False,
        "free": True,
        "description": "Modo simulado sin IA para pruebas y demos",
        "docs_url": None
    }
}

# Configuraciones por defecto
DEFAULT_SETTINGS = {
    "max_tokens": 800,
    "temperature": 0.7,
    "timeout": 60
}

# Variables de entorno para API keys
def get_api_key(provider: str) -> str:
    """Obtiene la API key desde variables de entorno"""
    key_map = {
        "huggingface_free": "HUGGINGFACE_API_KEY",
        "openai": "OPENAI_API_KEY", 
        "anthropic": "ANTHROPIC_API_KEY",
        "cohere": "COHERE_API_KEY",
        "groq": "GROQ_API_KEY",
        "together": "TOGETHER_API_KEY"
    }
    
    return os.getenv(key_map.get(provider, ""))

# Validaciones
def validate_provider(provider: str) -> bool:
    """Valida si un proveedor es válido"""
    return provider in API_CONFIGS

def validate_model(provider: str, model: str) -> bool:
    """Valida si un modelo es válido para el proveedor dado"""
    if not validate_provider(provider):
        return False
    return model in API_CONFIGS[provider]["models"]

# Funciones de utilidad
def get_provider_info(provider: str) -> dict:
    """Obtiene información completa del proveedor"""
    return API_CONFIGS.get(provider, {})

def get_free_providers() -> list:
    """Obtiene lista de proveedores gratuitos"""
    return [
        provider for provider, config in API_CONFIGS.items() 
        if config.get("free") == True
    ]

def get_paid_providers() -> list:
    """Obtiene lista de proveedores de pago"""
    return [
        provider for provider, config in API_CONFIGS.items() 
        if config.get("free") == False
    ]