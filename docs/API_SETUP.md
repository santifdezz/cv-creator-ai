# 🤖 Guía de Configuración de APIs

Esta guía te ayudará a configurar las diferentes APIs de IA disponibles en el CVisionAI.

## 🆓 APIs Gratuitas (Recomendadas para empezar)

### 1. **⚡ Groq (Recomendado - Rápido y Gratis)**

Groq ofrece inferencia súper rápida y gratuita de modelos open-source.

**Pasos:**
1. Ve a [console.groq.com](https://console.groq.com)
2. Regístrate con tu email
3. Ve a "API Keys" en el menú lateral
4. Crea una nueva API key
5. Copia la key (empieza con `gsk_`)
6. Añade a tu `.env`: `GROQ_API_KEY=gsk_tu-key-aquí`

**Modelos disponibles:**
- Llama 2 70B (excelente calidad)
- Mixtral 8x7B (muy rápido)
- Gemma 7B (ligero y eficiente)

**Límites:** Generoso para uso personal y desarrollo

---

### 2. **🤗 Hugging Face (Gratis con límites)**

Acceso gratuito a modelos open-source con algunos límites de uso.

**Pasos:**
1. Ve a [huggingface.co](https://huggingface.co)
2. Regístrate con tu email
3. Ve a Settings > Access Tokens
4. Crea un nuevo token (permisos de lectura)
5. Copia el token (empieza con `hf_`)
6. Añade a tu `.env`: `HUGGINGFACE_API_KEY=hf_tu-key-aquí`

**Límites:** 1000 requests/mes en el tier gratuito

---

### 3. **🏠 Ollama Local (Completamente gratis)**

Ejecuta modelos de IA directamente en tu computadora, sin APIs ni límites.

**Instalación:**

**Windows:**
```bash
# Descarga e instala desde https://ollama.ai
# O usando winget:
winget install Ollama.Ollama
```

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Descargar modelos:**
```bash
# Modelos recomendados para CV
ollama pull llama2          # Modelo general 7B
ollama pull mistral         # Rápido y eficiente 7B
ollama pull neural-chat     # Especializado en conversación
ollama pull codellama       # Para contenido técnico
```

**Verificar instalación:**
```bash
ollama list
```

La aplicación detectará automáticamente si Ollama está ejecutándose.

---

## 💳 APIs Premium (Mejor calidad)

### 4. **🤖 OpenAI (GPT-3.5/4)**

La API más popular y conocida, excelente calidad de generación.

**Pasos:**
1. Ve a [platform.openai.com](https://platform.openai.com)
2. Crea una cuenta y añade método de pago
3. Ve a "API Keys" y crea una nueva
4. Copia la key (empieza con `sk-`)
5. Añade a tu `.env`: `OPENAI_API_KEY=sk-tu-key-aquí`

**Costos aproximados por CV:**
- GPT-3.5 Turbo: ~$0.002-0.005
- GPT-4: ~$0.03-0.06
- GPT-4 Turbo: ~$0.01-0.03

**Recomendación:** Empieza con GPT-3.5 Turbo para pruebas

---

### 5. **🧠 Anthropic Claude**

Excelente para escritura profesional y contenido bien estructurado.

**Pasos:**
1. Ve a [console.anthropic.com](https://console.anthropic.com)
2. Crea una cuenta y añade método de pago
3. Ve a "API Keys" y crea una nueva
4. Copia la key (empieza con `sk-ant-`)
5. Añade a tu `.env`: `ANTHROPIC_API_KEY=sk-ant-tu-key-aquí`

**Costos aproximados por CV:**
- Claude Haiku: ~$0.001-0.003
- Claude Sonnet: ~$0.003-0.015
- Claude Opus: ~$0.015-0.075

---

### 6. **🚀 Cohere (Tier gratuito disponible)**

Buen balance entre calidad y precio, con tier gratuito mensual.

**Pasos:**
1. Ve a [dashboard.cohere.ai](https://dashboard.cohere.ai)
2. Regístrate con tu email
3. Ve a "API Keys" y crea una nueva
4. Copia la key
5. Añade a tu `.env`: `COHERE_API_KEY=tu-key-aquí`

**Tier gratuito:** Incluye suficientes tokens para pruebas mensuales

---

## 🔧 Configuración Adicional

### Variables de Entorno Opcionales

Puedes añadir estas configuraciones adicionales a tu `.env`:

```bash
# Puerto de la aplicación
PORT=7860

# Modo debug
DEBUG=false

# Timeout para APIs (segundos)
API_TIMEOUT=60

# Límite de tokens por request
MAX_TOKENS=800

# Temperatura de generación (0.0-1.0)
TEMPERATURE=0.7
```

---

## 🚦 Orden de Prioridad Recomendado

**Para empezar (gratis):**
1. **Modo Simulado** - Para probar la aplicación
2. **Groq** - Rápido y gratuito
3. **Ollama Local** - Si tienes RAM suficiente (8GB+)

**Para producción:**
1. **OpenAI GPT-3.5** - Calidad/precio balanceado
2. **Claude Sonnet** - Mejor calidad de escritura
3. **GPT-4** - Máxima calidad

---

## ❗ Consejos Importantes

### Seguridad
- ✅ Nunca subas tu archivo `.env` a repositorios públicos
- ✅ Usa `.gitignore` para excluir archivos sensibles
- ✅ Rota tus API keys regularmente
- ✅ Monitorea el uso de tus APIs

### Optimización de Costos
- 💡 Empieza siempre con APIs gratuitas para pruebas
- 💡 Usa Ollama Local para desarrollo intensivo
- 💡 Monitorea el uso en los dashboards de las APIs
- 💡 Implementa cache local para evitar requests duplicados

### Troubleshooting
- 🔍 Verifica que las API keys estén correctas
- 🔍 Revisa los logs en la consola para errores
- 🔍 Comprueba tu saldo/créditos en los dashboards
- 🔍 Asegúrate de que los modelos estén disponibles

---

## 📊 Comparativa Rápida

| API | Costo | Velocidad | Calidad | Setup |
|-----|-------|-----------|---------|-------|
| **Simulado** | Gratis | ⚡⚡⚡ | ⭐⭐⭐ | ✅ Sin config |
| **Groq** | Gratis | ⚡⚡⚡ | ⭐⭐⭐⭐ | 🔑 API key |
| **Ollama** | Gratis | ⚡⚡ | ⭐⭐⭐⭐ | 💻 Instalación |
| **OpenAI** | De pago | ⚡⚡ | ⭐⭐⭐⭐⭐ | 🔑 API key + 💳 |
| **Claude** | De pago | ⚡⚡ | ⭐⭐⭐⭐⭐ | 🔑 API key + 💳 |
| **Cohere** | Freemium | ⚡⚡ | ⭐⭐⭐⭐ | 🔑 API key |