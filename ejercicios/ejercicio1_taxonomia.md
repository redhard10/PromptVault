# Ejercicio 1: Diseño de Taxonomía y Ficha de Metadatos

## Contexto Teórico (Guadián, 2025)
La eficiencia de una biblioteca de prompts se basa en encontrar la instrucción adecuada en el menor tiempo posible. Para evitar la duplicidad y acelerar la búsqueda de prompts, se utilizan tres elementos de clasificación:
1. **Taxonomía multidimensional**: Carpetas organizadas por áreas de negocio y subtemas (ej. `marketing/redes_sociales/` o `legal/contratos/`).
2. **Etiquetas múltiples**: Permiten identificar la versatilidad de un prompt (ej. `#analisis`, `#redaccion`, `#servicio_al_cliente`).
3. **Metadatos estándar**: Atributos específicos que facilitan la autodocumentación y compatibilidad de cada prompt.

---

## 🎯 Instrucciones de la Tarea

La empresa consultora **Auctoritas** necesita estructurar su catálogo interno de prompts para tres áreas operativas: **Legal**, **Marketing** y **Recursos Humanos**.

Se te han entregado 3 prompts no catalogados (ver la sección "Material Inicial"). Debes realizar las siguientes tareas:
1. **Diseñar la taxonomía**: Define la ruta de carpetas (`Categoría/Subcategoría`) adecuada para cada uno de los 3 prompts.
2. **Asignar Etiquetas**: Define al menos 3 etiquetas descriptivas para cada prompt.
3. **Completar la Ficha de Metadatos**: Crea la cabecera estructurada para cada uno con los siguientes metadatos obligatorios:
   - `name`: Nombre descriptivo corto.
   - `version`: Versión de partida (suele ser `1.0.0`).
   - `description`: Breve descripción del caso de uso.
   - `compatible_models`: Modelos validados (ej. `Claude-3.5-Sonnet`, `GPT-4o`).
   - `variables`: Nombre de las variables encerradas en llaves `{}` que se usarán en el texto del prompt.
   - `rag_context`: Booleano (`true` o `false`) indicando si requiere que se le inyecte información de contexto externa.
   - `tags`: Array de etiquetas asignadas.

---

## 📝 Material Inicial (Prompts Desorganizados)

### Prompt A: Redacción de Oferta de Empleo
> "Eres un especialista en reclutamiento. Necesito que escribas un anuncio de trabajo atractivo para el puesto de {puesto} en el sector de {sector}. El anuncio debe detallar las principales responsabilidades que son {responsabilidades} y los requisitos obligatorios {requisitos}. El tono debe ser profesional y moderno."

### Prompt B: Análisis de Cláusulas de Confidencialidad
> "Actúa como un abogado corporativo experto. Analiza el siguiente contrato de confidencialidad (NDA) provisto en el contexto {documento_nda}. Identifica si existen cláusulas desfavorables o abusivas relativas a la duración de la confidencialidad que es de {duracion} y define las penalizaciones por incumplimiento {penalizaciones}. Genera un reporte detallando los riesgos encontrados."

### Prompt C: Calendario Editorial para LinkedIn
> "Eres un estratega de contenido digital. Crea un calendario de publicaciones para LinkedIn para la semana del {fecha_inicio}. La temática principal es {tema} y el objetivo es atraer prospectos B2B para nuestro producto {nombre_producto}. Genera una tabla con el día, el gancho (hook), el cuerpo del post y los hashtags recomendados."

---

## 📥 Plantilla de Entrega

Crea un archivo en tu espacio de trabajo llamado `ejercicios/respuestas/ejercicio1_solucion.md` (o copia esta estructura en la herramienta interactiva del panel web) y completa la ficha para cada prompt siguiendo este esquema:

```markdown
# Solución Ejercicio 1

## Prompt A: Redacción de Oferta de Empleo
- **Ruta Taxonómica**: `recursos_humanos/reclutamiento/`
- **Metadatos**:
  - Nombre: [Nombre descriptivo]
  - Versión: 1.0.0
  - Descripción: [Escribe el caso de uso]
  - Modelos Compatibles: [Modelos]
  - Variables requeridas: `{puesto}`, `{sector}`, `{responsabilidades}`, `{requisitos}`
  - RAG Context: [true / false]
  - Etiquetas: [tag1, tag2, tag3]

## Prompt B: Análisis de Cláusulas de Confidencialidad
- **Ruta Taxonómica**: [Ruta]
- **Metadatos**:
  ... (completar)

...
```
