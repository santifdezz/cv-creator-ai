# Generador Automático de CV y Cartas de Presentación

---

## Descripción

Esta aplicación web permite a los usuarios generar automáticamente currículums y cartas de presentación personalizadas a partir de sus datos ingresados en un formulario. El contenido es generado por un modelo de inteligencia artificial y el usuario puede descargar directamente el PDF desde la página.

---

## Funcionalidades

- Formulario para ingresar datos personales, experiencia laboral, educación, habilidades y objetivos profesionales.
- Generación automática de currículum y carta de presentación personalizada mediante IA.
- Descarga directa del currículum y carta en formato PDF.
- Interfaz sencilla y responsiva.
- Despliegue en Vercel o Hugging Face Spaces con Gradio.

---

## Stack Tecnológico

| Componente                | Tecnología / Herramienta                      | Justificación                                       |
|--------------------------|----------------------------------------------|----------------------------------------------------|
| Frontend                 | React / Next.js / Gradio                      | Framework ligero, fácil de desplegar en Vercel y Hugging Face. Gradio facilita la integración rápida con IA. |
| Backend (API IA)         | Hugging Face Inference API (modelos gratuitos) | Usar modelos gratuitos de Hugging Face para generación de texto. |
| Generación PDF           | jsPDF / PDFLib / Puppeteer                    | Para crear PDFs dinámicos desde el frontend.       |
| Hosting                  | Vercel / Hugging Face Spaces                   | Vercel para Next.js o frontend React; Hugging Face Spaces para demos con Gradio. |
| Integración IA           | API Hugging Face o modelo local con Gradio    | Permite usar IA sin coste inicial.                  |

---

## Instalación y despliegue

1. Clonar el repositorio:  
   ```bash
   git clone https://github.com/santifdezz/cv-creator-ai.git
   cd cv-creator-ai
   ```
2. Instalar dependencias (suponiendo un proyecto React / Next.js):
    ```bash
    npm install
    ```

3. Configurar la clave API de Hugging Face (si usas su API externa):

   Crear un archivo .env.local con:
    ```bash
    HUGGINGFACE_API_KEY=tu_api_key_aqui
    ```

4. Ejecutar en modo desarrollo:

   
    ```bash
    npm run dev
    ```
5. Desplegar en Vercel con el comando:
    ```bash
    vercel
    ```

    o en Hugging Face Spaces, subir directamente el proyecto con Gradio.

---
## Uso

- El usuario rellena el formulario con sus datos.

- La IA genera un texto estructurado para CV y carta.

- El frontend genera un PDF descargable.

- El usuario descarga ambos archivos directamente.

---
## Futuras mejoras

- Añadir plantillas personalizables para CV.

- Integrar validaciones de datos.

- Servicio premium con revisión humana.

- Adaptar CVs para diferentes sectores y ATS.

- Implementar versión multilingüe (español / inglés).

---
## Licencia

MIT License.

