# 🚀 Guía de Despliegue - CV Generator AI

Esta guía cubre las diferentes opciones para desplegar tu aplicación CV Generator AI en producción.

## 🎯 Opciones de Despliegue

### 1. **🤗 Hugging Face Spaces (Recomendado - Gratis)**

Hugging Face Spaces es la opción más fácil y gratuita para desplegar aplicaciones Gradio.

#### **Ventajas:**
- ✅ Completamente gratuito
- ✅ HTTPS automático
- ✅ Fácil configuración
- ✅ Git-based deployment
- ✅ Variables de entorno seguras

#### **Pasos de despliegue:**

1. **Crear un Space:**
   - Ve a [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Selecciona "Gradio" como SDK
   - Elige un nombre descriptivo (ej: `cv-generator-ai`)

2. **Configurar el repositorio:**
   ```bash
   # Clonar el space
   git clone https://huggingface.co/spaces/tu-usuario/cv-generator-ai
   cd cv-generator-ai
   
   # Copiar archivos del proyecto (excluyendo .venv, __pycache__, etc)
   cp -r /path/to/your/project/* .
   
   # No copies estos archivos/carpetas:
   # - .venv/
   # - __pycache__/
   # - .env (usa variables de entorno en su lugar)
   ```

3. **Configurar variables de entorno:**
   - Ve a Settings de tu Space
   - En "Repository secrets" añade tus API keys:
     ```
     GROQ_API_KEY=gsk_tu-key-aqui
     OPENAI_API_KEY=sk-tu-key-aqui
     ANTHROPIC_API_KEY=sk-ant-tu-key-aqui
     ```

4. **Subir cambios:**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push
   ```

5. **¡Listo!** Tu app estará disponible en:
   `https://huggingface.co/spaces/tu-usuario/cv-generator-ai`

---

### 2. **🐳 Docker (Para servidores propios)**

Ideal si tienes tu propio servidor o quieres más control.

#### **Construcción local:**
```bash
# Construir imagen
docker build -t cv-generator-ai .

# Ejecutar contenedor
docker run -p 7860:7860 \
  -e GROQ_API_KEY=tu-key \
  -e OPENAI_API_KEY=tu-key \
  cv-generator-ai
```

#### **Docker Compose (recomendado):**

Crear `docker-compose.yml`:
```yaml
version: '3.8'

services:
  cv-generator:
    build: .
    ports:
      - "7860:7860"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./data:/app/data  # Para persistir datos si es necesario
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7860/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Ejecutar:
```bash
# Crear archivo .env con tus API keys
echo "GROQ_API_KEY=tu-key" > .env
echo "OPENAI_API_KEY=tu-key" >> .env

# Levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f
```

---

### 3. **☁️ Railway (Fácil y económico)**

Railway ofrece despliegue directo desde GitHub con un tier gratuito generoso.

#### **Pasos:**

1. **Conectar repositorio:**
   - Ve a [railway.app](https://railway.app)
   - "Start a New Project" → "Deploy from GitHub repo"
   - Selecciona tu repositorio

2. **Configurar variables:**
   - En tu proyecto Railway, ve a "Variables"
   - Añade tus API keys:
     ```
     GROQ_API_KEY=gsk_tu-key-aqui
     OPENAI_API_KEY=sk-tu-key-aqui
     PORT=7860
     ```

3. **Configurar build:**
   Railway detectará automáticamente Python y usará `requirements.txt`

4. **Custom start command (opcional):**
   Si necesitas un comando personalizado:
   ```bash
   python app.py
   ```

**Límites del tier gratuito:** $5 USD/mes de créditos

---

### 4. **▲ Vercel (Para aplicaciones serverless)**

Vercel requiere adaptaciones ya que Gradio no es nativamente serverless.

#### **Opción A: Usar Gradio en modo API**

Crear `api/generate.py`:
```python
from gradio import Interface
import os

def create_api():
    # Tu lógica de generación de CV aquí
    pass

# Exportar como función serverless
app = create_api()
```

#### **Opción B: Usar alternativa ligera**

Considera usar FastAPI + HTML/JS en lugar de Gradio para Vercel.

---

### 5. **🔵 Azure Container Instances**

Para empresas que prefieren Azure:

```bash
# Crear grupo de recursos
az group create --name cv-generator-rg --location eastus

# Desplegar contenedor
az container create \
  --resource-group cv-generator-rg \
  --name cv-generator \
  --image tu-registro/cv-generator-ai:latest \
  --ports 7860 \
  --environment-variables \
    GROQ_API_KEY=tu-key \
    OPENAI_API_KEY=tu-key
```

---

### 6. **🟠 AWS ECS/Fargate**

Para despliegues enterprise en AWS:

1. **Crear ECR repository:**
   ```bash
   aws ecr create-repository --repository-name cv-generator-ai
   ```

2. **Subir imagen:**
   ```bash
   docker tag cv-generator-ai:latest your-account.dkr.ecr.region.amazonaws.com/cv-generator-ai:latest
   docker push your-account.dkr.ecr.region.amazonaws.com/cv-generator-ai:latest
   ```

3. **Crear task definition y service** usando la consola de AWS ECS

---

## 🔧 Configuraciones de Producción

### **Variables de entorno importantes:**

```bash
# Básicas
PORT=7860
DEBUG=false

# APIs
GROQ_API_KEY=tu-key
OPENAI_API_KEY=tu-key
ANTHROPIC_API_KEY=tu-key

# Configuración de producción
API_TIMEOUT=30
MAX_CONCURRENT_REQUESTS=10
RATE_LIMIT_PER_MINUTE=60

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log

# Seguridad
ALLOWED_ORIGINS=https://tu-dominio.com
CORS_ENABLED=true
```

### **Optimizaciones para producción:**

1. **Caché de respuestas:**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def cached_ai_generation(prompt_hash):
       # Tu lógica aquí
       pass
   ```

2. **Rate limiting:**
   ```python
   from slowapi import Limiter, _rate_limit_exceeded_handler
   from slowapi.util import get_remote_address
   
   limiter = Limiter(key_func=get_remote_address)
   ```

3. **Health checks:**
   ```python
   @app.get("/health")
   def health_check():
       return {"status": "healthy", "version": "1.0.0"}
   ```

---

## 🔒 Seguridad en Producción

### **1. Variables de entorno:**
- ✅ Nunca hardcodees API keys
- ✅ Usa servicios de secrets management
- ✅ Rota keys regularmente

### **2. HTTPS:**
- ✅ Siempre usa HTTPS en producción
- ✅ Configura certificados SSL válidos
- ✅ Redirige HTTP a HTTPS

### **3. CORS:**
```python
# En app.py, configurar CORS apropiadamente
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
```

### **4. Input validation:**
- ✅ Valida todos los inputs del usuario
- ✅ Sanitiza datos antes de procesarlos
- ✅ Implementa rate limiting

---

## 📊 Monitoreo y Logs

### **1. Logging estructurado:**
```python
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### **2. Métricas importantes:**
- 📈 Número de CVs generados
- ⏱️ Tiempo de respuesta promedio
- 🚨 Rate de errores
- 💰 Costo de APIs
- 👥 Usuarios activos

### **3. Alertas:**
- 🚨 Error rate > 5%
- 💸 Costo de API > límite mensual
- ⏱️ Response time > 30s
- 🔴 Health check fails

---

## 🚀 Deployment Checklist

Antes de desplegar a producción:

- [ ] ✅ Variables de entorno configuradas
- [ ] ✅ API keys válidas y con límites apropiados
- [ ] ✅ HTTPS configurado
- [ ] ✅ Logging habilitado
- [ ] ✅ Health checks funcionando
- [ ] ✅ Rate limiting implementado
- [ ] ✅ Error handling robusto
- [ ] ✅ Monitoreo configurado
- [ ] ✅ Backup strategy definida
- [ ] ✅ Testing en environment de staging
- [ ] ✅ Documentación actualizada

---

## 💡 Recomendaciones por Caso de Uso

### **🏠 Uso Personal/Demo:**
- **Hugging Face Spaces** (gratis, fácil)

### **🏢 Startup/Pequeña empresa:**
- **Railway** o **Render** (económico, escalable)

### **🏭 Empresa mediana:**
- **Docker** en **DigitalOcean** o **Linode**

### **🏬 Enterprise:**
- **AWS ECS/Fargate** o **Azure Container Instances**

---

## 🆘 Troubleshooting Común

### **Error: Module not found**
```bash
# Verificar requirements.txt está completo
pip freeze > requirements.txt
```

### **Error: API key invalid**
```bash
# Verificar variables de entorno
echo $GROQ_API_KEY
```

### **Error: Port already in use**
```bash
# Cambiar puerto en variables de entorno
export PORT=8080
```

### **Error: Out of memory**
```bash
# Optimizar para contenedores pequeños
export GRADIO_SERVER_NAME=0.0.0.0
export GRADIO_ANALYTICS_ENABLED=false
```