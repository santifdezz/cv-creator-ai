"""
Servicio de IA para generación de contenido de CV

Este módulo maneja todas las llamadas a las diferentes APIs de IA
y proporciona funcionalidad de fallback en caso de errores.
"""

import requests
import json
import asyncio
from typing import Dict, Any, Optional
from .config import API_CONFIGS, DEFAULT_SETTINGS, get_api_key
from .content_generator import ContentGenerator

class AIService:
    def __init__(self):
        self.content_generator = ContentGenerator()
        self.session = requests.Session()
        
    async def generate_cv_content(self, form_data: Dict[str, Any], api_provider: str, 
                                 model_name: str, api_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Genera contenido del CV usando diferentes APIs de IA
        """
        
        # Crear prompt estructurado
        prompt = self._create_cv_prompt(form_data)
        
        # Llamar a la API correspondiente
        try:
            if api_provider == "huggingface_free" and api_key:
                ai_response = await self._call_huggingface_api(model_name, prompt, api_key)
            elif api_provider == "openai" and api_key:
                ai_response = await self._call_openai_api(model_name, prompt, api_key)
            elif api_provider == "anthropic" and api_key:
                ai_response = await self._call_anthropic_api(model_name, prompt, api_key)
            elif api_provider == "cohere" and api_key:
                ai_response = await self._call_cohere_api(model_name, prompt, api_key)
            elif api_provider == "groq" and api_key:
                ai_response = await self._call_groq_api(model_name, prompt, api_key)
            elif api_provider == "together" and api_key:
                ai_response = await self._call_together_api(model_name, prompt, api_key)
            elif api_provider == "ollama_local":
                ai_response = await self._call_ollama_local(model_name, prompt)
            elif api_provider == "mock":
                ai_response = "mock_response"
            else:
                raise Exception("Configuración de API inválida o API key faltante")
            
            # Procesar respuesta
            if ai_response.startswith("Error") or not ai_response or ai_response == "mock_response":
                return self.content_generator.generate_fallback_content(form_data)
            
            # Parsear JSON de la respuesta
            try:
                cleaned_response = self._clean_ai_response(ai_response)
                ai_content = json.loads(cleaned_response)
                
                # Validar estructura
                if not self._validate_ai_response(ai_content):
                    raise Exception("Estructura JSON inválida")
                
                return ai_content
                
            except (json.JSONDecodeError, Exception):
                return self.content_generator.generate_fallback_content(form_data)
                
        except Exception as e:
            print(f"Error en generación IA: {e}")
            return self.content_generator.generate_fallback_content(form_data)

    def _create_cv_prompt(self, form_data: Dict[str, Any]) -> str:
        """Crea el prompt estructurado para la IA"""
        
        prompt = f"""
Actúa como un experto en recursos humanos y escritor profesional de CVs. 
Genera un currículum profesional y optimizado para ATS basado en los siguientes datos:

DATOS PERSONALES:
- Nombre: {form_data['nombre']}
- Email: {form_data['email']}
- Teléfono: {form_data['telefono']}
- LinkedIn: {form_data.get('linkedin', 'No especificado')}
- Ubicación: {form_data.get('ubicacion', 'No especificado')}

PERFIL PROFESIONAL:
- Objetivo profesional: {form_data.get('objetivo', 'No especificado')}
- Años de experiencia: {form_data.get('experiencia_anos', 'No especificado')}

EXPERIENCIA LABORAL:
{form_data.get('experiencia_laboral', 'No especificado')}

EDUCACIÓN:
{form_data.get('educacion', 'No especificado')}

HABILIDADES:
{form_data.get('habilidades', 'No especificado')}

IDIOMAS:
{form_data.get('idiomas', 'No especificado')}

INSTRUCCIONES:
1. Crea un resumen profesional atractivo de 3-4 líneas que destaque el valor único del candidato
2. Reformula y optimiza la experiencia laboral con verbos de acción y logros cuantificables
3. Organiza las habilidades por categorías (técnicas, blandas, herramientas)
4. Asegúrate de que el contenido esté optimizado para ATS
5. Usa un lenguaje profesional pero accesible
6. Prioriza la información más relevante

Responde SOLO con un JSON válido con esta estructura exacta:
{{
    "resumen_profesional": "texto del resumen profesional aquí",
    "experiencia_optimizada": [
        {{
            "puesto": "título del puesto",
            "empresa": "nombre empresa", 
            "periodo": "fechas",
            "descripcion": ["logro 1", "logro 2", "logro 3"]
        }}
    ],
    "habilidades_organizadas": {{
        "tecnicas": ["habilidad1", "habilidad2"],
        "blandas": ["habilidad1", "habilidad2"],
        "herramientas": ["herramienta1", "herramienta2"]
    }}
}}

NO incluyas texto adicional, comentarios o explicaciones. Solo el JSON válido.
"""
        return prompt

    def _clean_ai_response(self, response: str) -> str:
        """Limpia la respuesta de la IA para extraer JSON válido"""
        cleaned = response.strip()
        
        # Remover markdown
        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()
        elif cleaned.startswith("```"):
            cleaned = cleaned.replace("```", "").strip()
        
        # Buscar JSON en la respuesta
        start_idx = cleaned.find("{")
        end_idx = cleaned.rfind("}")
        
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx+1]
        
        return cleaned

    def _validate_ai_response(self, response: Dict[str, Any]) -> bool:
        """Valida que la respuesta de IA tenga la estructura correcta"""
        required_keys = ["resumen_profesional", "experiencia_optimizada", "habilidades_organizadas"]
        return all(key in response for key in required_keys)

    async def _call_huggingface_api(self, model_name: str, prompt: str, api_key: str) -> str:
        """Llamada a la API de Hugging Face"""
        headers = {"Authorization": f"Bearer {api_key}"}
        
        # Diferentes formatos según el modelo
        if "flan-t5" in model_name:
            payload = {"inputs": prompt, "parameters": {"max_length": DEFAULT_SETTINGS["max_tokens"]}}
        else:
            payload = {
                "inputs": prompt, 
                "parameters": {
                    "max_new_tokens": DEFAULT_SETTINGS["max_tokens"], 
                    "temperature": DEFAULT_SETTINGS["temperature"]
                }
            }
        
        try:
            response = self.session.post(
                f"{API_CONFIGS['huggingface_free']['endpoint']}{model_name}",
                headers=headers,
                json=payload,
                timeout=DEFAULT_SETTINGS["timeout"]
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").replace(prompt, "").strip()
                return str(result)
            else:
                return f"Error API HuggingFace: {response.status_code}"
        except Exception as e:
            return f"Error llamada HuggingFace: {str(e)}"

    async def _call_openai_api(self, model_name: str, prompt: str, api_key: str) -> str:
        """Llamada a la API de OpenAI"""
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": DEFAULT_SETTINGS["max_tokens"],
            "temperature": DEFAULT_SETTINGS["temperature"]
        }
        
        try:
            response = self.session.post(
                API_CONFIGS['openai']['endpoint'],
                headers=headers,
                json=payload,
                timeout=DEFAULT_SETTINGS["timeout"]
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Error API OpenAI: {response.status_code}"
        except Exception as e:
            return f"Error llamada OpenAI: {str(e)}"

    async def _call_anthropic_api(self, model_name: str, prompt: str, api_key: str) -> str:
        """Llamada a la API de Anthropic"""
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": model_name,
            "max_tokens": DEFAULT_SETTINGS["max_tokens"],
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = self.session.post(
                API_CONFIGS['anthropic']['endpoint'],
                headers=headers,
                json=payload,
                timeout=DEFAULT_SETTINGS["timeout"]
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["content"][0]["text"]
            else:
                return f"Error API Anthropic: {response.status_code}"
        except Exception as e:
            return f"Error llamada Anthropic: {str(e)}"

    async def _call_cohere_api(self, model_name: str, prompt: str, api_key: str) -> str:
        """Llamada a la API de Cohere"""
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model_name,
            "prompt": prompt,
            "max_tokens": DEFAULT_SETTINGS["max_tokens"],
            "temperature": DEFAULT_SETTINGS["temperature"]
        }
        
        try:
            response = self.session.post(
                API_CONFIGS['cohere']['endpoint'],
                headers=headers,
                json=payload,
                timeout=DEFAULT_SETTINGS["timeout"]
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["generations"][0]["text"]
            else:
                return f"Error API Cohere: {response.status_code}"
        except Exception as e:
            return f"Error llamada Cohere: {str(e)}"

    async def _call_groq_api(self, model_name: str, prompt: str, api_key: str) -> str:
        """Llamada a la API de Groq"""
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": DEFAULT_SETTINGS["max_tokens"],
            "temperature": DEFAULT_SETTINGS["temperature"]
        }
        
        try:
            response = self.session.post(
                API_CONFIGS['groq']['endpoint'],
                headers=headers,
                json=payload,
                timeout=DEFAULT_SETTINGS["timeout"]
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Error API Groq: {response.status_code}"
        except Exception as e:
            return f"Error llamada Groq: {str(e)}"

    async def _call_together_api(self, model_name: str, prompt: str, api_key: str) -> str:
        """Llamada a la API de Together AI"""
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model_name,
            "prompt": prompt,
            "max_tokens": DEFAULT_SETTINGS["max_tokens"],
            "temperature": DEFAULT_SETTINGS["temperature"]
        }
        
        try:
            response = self.session.post(
                API_CONFIGS['together']['endpoint'],
                headers=headers,
                json=payload,
                timeout=DEFAULT_SETTINGS["timeout"]
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["output"]["choices"][0]["text"]
            else:
                return f"Error API Together: {response.status_code}"
        except Exception as e:
            return f"Error llamada Together: {str(e)}"

    async def _call_ollama_local(self, model_name: str, prompt: str) -> str:
        """Llamada a Ollama local"""
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = self.session.post(
                API_CONFIGS['ollama_local']['endpoint'],
                json=payload,
                timeout=120  # Ollama puede ser más lento
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "Sin respuesta")
            else:
                return f"Error Ollama local: {response.status_code}"
        except Exception as e:
            return f"Error llamada Ollama: {str(e)} (¿Está Ollama ejecutándose?)"