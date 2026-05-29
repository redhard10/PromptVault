# Ejercicio 2: El Doble Formato (YAML + JSON)

## Contexto Teórico (Guadián, 2025)
Los prompts optimizados de una biblioteca deben servir para dos tipos de consumidores:
* **Humanos (Curadores y Editores)**: Necesitan un formato legible, fácil de redactar y versionar. Para esto, **Markdown con frontmatter YAML** es ideal, ya que permite definir metadatos en un bloque estructurado superior y redactar el prompt en texto plano enriquecido debajo.
* **Máquinas (Software, Scripts, APIs)**: Necesitan leer los metadatos de forma estructurada e inyectar variables automáticamente. El formato de intercambio de datos **JSON** es el estándar de oro para esta automatización.

### Ejemplo de Estructura de Doble Formato

**Archivo en Markdown (.md) con Frontmatter YAML:**
```yaml
---
name: "Respuesta Empática de Soporte"
version: "1.0.0"
description: "Generación de respuestas cordiales para agentes de atención al cliente."
compatible_models:
  - "gpt-4o"
  - "claude-3-5-sonnet"
variables:
  - "cliente"
  - "problema"
rag_context: false
tags:
  - "soporte"
  - "atencion_cliente"
  - "empatia"
---
Actúa como un agente de soporte. Responde a {cliente} sobre el problema {problema} con empatía.
```

**Archivo en JSON (.json):**
```json
{
  "name": "Respuesta Empática de Soporte",
  "version": "1.0.0",
  "description": "Generación de respuestas cordiales para agentes de atención al cliente.",
  "compatible_models": ["gpt-4o", "claude-3-5-sonnet"],
  "variables": ["cliente", "problema"],
  "rag_context": false,
  "tags": ["soporte", "atencion_cliente", "empatia"],
  "prompt_text": "Actúa como un agente de soporte. Responde a {cliente} sobre el problema {problema} con empatía."
}
```

---

## 🎯 Instrucciones de la Tarea

1. Toma el siguiente prompt de **Análisis de Sentimiento de Correos**:
   > "Analiza el tono emocional del siguiente correo electrónico enviado por un cliente: {correo_cliente}. Clasifica el sentimiento como POSITIVO, NEUTRO o NEGATIVO. Si es negativo, extrae los puntos de frustración principales: {puntos_frustracion}. Devuelve la respuesta en formato JSON."
2. Redacta el archivo completo en formato **Markdown con YAML Frontmatter**. Asegúrate de incluir todos los campos de metadatos vistos en el ejercicio 1.
3. Convierte manualmente esa estructura al formato **JSON** equivalente. Nota cómo el texto del prompt debe colocarse dentro de un campo llamado `"prompt_text"`.
4. Comprueba que tu JSON sea sintácticamente válido (puedes validarlo en la sección "Conversor" de la aplicación web interactiva).

---

## 📥 Plantilla de Entrega

Crea un archivo llamado `ejercicios/respuestas/ejercicio2_solucion.md` y copia allí tu versión Markdown-YAML y tu versión JSON. El formato debe lucir así:

```markdown
# Solución Ejercicio 2

## 1. Archivo Markdown (.md)
(Copia aquí tu archivo con delimitadores --- para el frontmatter y el texto del prompt abajo)

## 2. Archivo JSON (.json)
```json
{
  // Tu JSON aquí
}
```
```
