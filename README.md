---
title: CVision
emoji: 🔥
colorFrom: pink
colorTo: yellow
sdk: gradio
sdk_version: 5.45.0
app_file: app.py
pinned: false
license: mit
short_description: CVision - AI Curriculum Vitae Generator 
---

# Generador Automático de CV y Cartas de Presentación 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/gradio-4.43+-orange.svg)](https://gradio.app/)

---

## 📝 Descripción

Una aplicación web moderna que utiliza **múltiples APIs de inteligencia artificial** para generar currículums profesionales optimizados para ATS (Applicant Tracking Systems). Diseñado con flexibilidad para usar tanto **opciones gratuitas como premium**.

![Screenshot de la aplicación](https://fpoimg.com/800x400?text=CV+Generator+AI&bg_color=e6e6e6&text_color=1e3a8a)

---

## ✨ Características

###  **Múltiples Proveedores de IA**
- **🆓 Opciones Gratuitas:**
  - 🎭 **Modo Simulado**: Sin API, usa plantillas inteligentes
  - 🏠 **Ollama Local**: Ejecuta modelos en tu PC (Llama 2, Mistral, etc.)
  - 🤗 **Hugging Face**: API gratuita con límites de uso
  - ⚡ **Groq**: Inferencia súper rápida y gratuita

- **💳 Opciones Premium:**
  - 🤖 **OpenAI**: GPT-3.5/4 (excelente calidad)
  - 🧠 **Anthropic**: Claude (ideal para escritura)
  - 🚀 **Cohere**: Con tier gratuito mensual

###  **CV Profesional y Optimizado**
- ✅ **Compatible con ATS** (Applicant Tracking Systems)
- ✅ **Diseño moderno** según estándares 2025
- ✅ **Formato PDF profesional** con ReportLab
- ✅ **Categorización inteligente** de habilidades
- ✅ **Contenido optimizado** por IA o plantillas avanzadas

### **Funcionalidades Avanzadas**
- 🔧 **Arquitectura modular** fácil de extender
- 🌐 **Interfaz web intuitiva** con Gradio
- 📱 **Diseño responsive** para móviles
- 🛡️ **Validaciones robustas** de datos
- 🔄 **Sistema de fallback** automático

---

## 🚀 Inicio Rápido

### Opción 1: Uso Inmediato (Modo Simulado)
```bash
# Clona el repositorio
git clone https://github.com/santifdezz/cv-creator-ai.git
cd cv-creator-ai

# Instala dependencias
pip install -r requirements.txt

# Ejecuta la aplicación
python app.py
```

¡Ya puedes usar la aplicación sin ninguna API! El modo simulado genera CVs profesionales usando plantillas inteligentes.

### Opción 2: Con IA (Recomendado)

#### 🆓 **Configuración Gratuita - Groq (Recomendado)**
```bash
# 1. Regístrate en https://console.groq.com (gratis)
# 2. Obtén tu API key
# 3. Crea un archivo .env
cp .env.example .env

# 4. Edita .env y añade:
# GROQ_API_KEY=gsk_tu-key-aquí
```

#### 🏠 **Configuración Local - Ollama**
```bash
# Instala Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Descarga un modelo (ejemplo: Llama 2)
ollama pull llama2

# Ejecuta la aplicación (detecta Ollama automáticamente)
python app.py
```

## 📦 Instalación Completa

### Requisitos
- Python 3.8+
- pip

### Instalación
```bash
# Clona el repositorio
git clone https://github.com/santifdezz/cv-creator-ai.git
cd cv-creator-ai

# Crea un entorno virtual (recomendado)
python -m venv venv

# Activa el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instala las dependencias
pip install -r requirements.txt

# (Opcional) Configura las API keys
cp .env.example .env
# Edita .env con tus API keys
```

### Ejecutar la aplicación
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:7860`

## 🤖 Guía de APIs

### 🆓 **APIs Gratuitas (Recomendadas para empezar)**

| Proveedor | Velocidad | Calidad | Setup | Límites |
|-----------|-----------|---------|-------|---------|
| **🎭 Simulado** | ⚡ Instantáneo | ⭐⭐⭐ | ✅ Sin configuración | ♾️ Ilimitado |
| **⚡ Groq** | ⚡⚡⚡ Muy rápido | ⭐⭐⭐⭐ | 🔑 Requiere key gratuita | 🆓 Generoso |
| **🏠 Ollama** | ⚡⚡ Rápido | ⭐⭐⭐⭐ | 💻 Instalación local | ♾️ Ilimitado |
| **🤗 Hugging Face** | ⚡ Lento | ⭐⭐⭐ | 🔑 Requiere key gratuita | 📊 Limitado |

### 💳 **APIs Premium (Mejor calidad)**

| Proveedor | Costo Aprox. | Calidad | Especialidad |
|-----------|---------------|---------|--------------|
| **🤖 OpenAI GPT-3.5** | ~$0.002/CV | ⭐⭐⭐⭐ | General |
| **🤖 OpenAI GPT-4** | ~$0.03/CV | ⭐⭐⭐⭐⭐ | Máxima calidad |
| **🧠 Claude** | ~$0.01/CV | ⭐⭐⭐⭐⭐ | Escritura profesional |
| **🚀 Cohere** | Tier gratuito | ⭐⭐⭐⭐ | Texto optimizado |

## 🗂️ Estructura del Proyecto

```
cv-creator-ai/
├── app.py                 # Aplicación principal Gradio
├── requirements.txt       # Dependencias Python
├── Dockerfile            # Para despliegue en contenedor
├── .env.example          # Plantilla de variables de entorno
├── README.md             # Documentación
│
├── src/                  # Código fuente modular
│   ├── __init__.py       # Inicialización del paquete
│   ├── config.py         # Configuración de APIs
│   ├── ai_service.py     # Servicio de llamadas a IA
│   ├── content_generator.py  # Generador sin IA (fallback)
│   ├── pdf_generator.py  # Generador de PDFs
│   └── utils.py          # Utilidades y validaciones
│
└── docs/                 # Documentación adicional
    ├── API_SETUP.md      # Guía de configuración de APIs
    └── DEPLOYMENT.md     # Guía de despliegue
```

## 🔧 Configuración de APIs

### Obtener API Keys Gratuitas

#### 1. **Groq (Recomendado - Gratis y Rápido)**
```bash
# 1. Ve a https://console.groq.com
# 2. Regístrate gratis
# 3. Ve a "API Keys" 
# 4. Crea una nueva key
# 5. Añade a .env: GROQ_API_KEY=gsk_tu-key-aquí
```

#### 2. **Hugging Face (Gratis con límites)**
```bash
# 1. Ve a https://huggingface.co
# 2. Regístrate gratis
# 3. Ve a Settings > Access Tokens
# 4. Crea un nuevo token
# 5. Añade a .env: HUGGINGFACE_API_KEY=hf_tu-key-aquí
```

#### 3. **Ollama (Completamente local y gratis)**
```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Descargar modelos (ejemplos)
ollama pull llama2        # Modelo general 7B
ollama pull mistral       # Modelo rápido 7B
ollama pull neural-chat   # Especializado en chat
```

### APIs Premium (Mayor Calidad)

<details>
<summary>🤖 OpenAI (GPT-3.5/4) - Click para expandir</summary>

```bash
# 1. Ve a https://platform.openai.com
# 2. Crea una cuenta y añade método de pago
# 3. Ve a API Keys y crea una nueva
# 4. Añade a .env: OPENAI_API_KEY=sk-tu-key-aquí

# Costos aproximados:
# GPT-3.5 Turbo: ~$0.002 por CV
# GPT-4: ~$0.03-0.06 por CV
```
</details>

<details>
<summary>🧠 Anthropic Claude - Click para expandir</summary>

```bash
# 1. Ve a https://console.anthropic.com
# 2. Crea una cuenta y añade método de pago
# 3. Ve a API Keys y crea una nueva
# 4. Añade a .env: ANTHROPIC_API_KEY=sk-ant-tu-key-aquí

# Costos aproximados:
# Claude Haiku: ~$0.001-0.003 por CV
# Claude Sonnet: ~$0.003-0.015 por CV
# Claude Opus: ~$0.015-0.075 por CV
```
</details>

## 🚀 Despliegue

### Hugging Face Spaces (Recomendado)
```bash
# 1. Ve a https://huggingface.co/spaces
# 2. Crea un nuevo Space con SDK=Gradio
# 3. Sube los archivos del proyecto
# 4. Añade tus API keys en Settings > Variables
```

### Docker
```bash
# Construir imagen
docker build -t cvision .

# Ejecutar contenedor
docker run -p 7860:7860 \
  -e GROQ_API_KEY=tu-key \
  cvision
```

### Vercel/Netlify
Ver [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) para instrucciones detalladas.

## 💡 Uso de la Aplicación

### 1. **Configura tu IA**
- Selecciona un proveedor (recomendamos Groq para empezar)
- Si es necesario, añade tu API key
- Elige el modelo específico

### 2. **Completa tus datos**
- **Obligatorios**: Nombre, Email, Teléfono
- **Opcionales**: LinkedIn, Ubicación, Experiencia, etc.

### 3. **Genera tu CV**
- Haz click en "🤖 Generar CV con IA"
- Espera unos segundos
- ¡Descarga tu CV profesional!

### 4. **Personaliza**
- Revisa el contenido generado
- Ajusta según la oferta específica
- Regenera si es necesario

## 📊 Ejemplos de Calidad

### Entrada del Usuario:
```
Experiencia: Desarrollador - TechCorp - 2020-2024
Habilidades: JavaScript, React, Python
```

### Salida Optimizada por IA:
```
🎯 Resumen Profesional:
"Desarrollador Full Stack con 4+ años de experiencia especializando en tecnologías web modernas. Expertise en JavaScript, React y Python con historial comproba
---
## 🛠️ Futuras mejoras

- Añadir plantillas personalizables para CV.

- Integrar validaciones de datos.

- Servicio premium con revisión humana.

- Adaptar CVs para diferentes sectores y ATS.

- Implementar versión multilingüe (español / inglés).

---
## 📄 Licencia

MIT License.

