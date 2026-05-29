# Ejercicio 5: Gobernanza, Control de Versiones y Modelos

## Contexto Teórico
Un catálogo de prompts sin gobernanza se deteriora rápidamente y se convierte en lo que Carlos Guadián (2025) llama un **"basurero digital"**. Para evitarlo, se definen políticas de control de versiones y flujo de trabajo:

* **Control de Versiones (Versionado)**:
  - Cambios menores (ej. corregir ortografía, reescribir una frase aclaratoria): Incremento en el parche (de `1.0.0` a `1.0.1`).
  - Cambios en las variables o en la lógica de procesamiento (ej. agregar `{NUEVA_VARIABLE}`): Incremento menor (de `1.0.0` a `1.1.0`).
  - Cambios de comportamiento radical o cambio de modelo de destino: Incremento mayor (de `1.0.0` a `2.0.0`).
* **Roles de Gobernanza**:
  - **Curador de Prompts (Auditor)**: Posee permiso de escritura total, valida la calidad de las salidas del prompt con métricas de evaluación y aprueba el pase a producción.
  - **Editor (Ingeniero de Prompts)**: Propone nuevas plantillas o modificaciones de las existentes. Trabaja en ramas de Git o en estado de "Borrador".
  - **Lector**: Consumidor final del prompt (ej. agentes de atención, redactores) que solo tiene permiso de lectura y uso del catálogo.

---

## 🎯 Instrucciones de la Tarea

La consultora **Auctoritas** tiene un prompt en producción para el área financiera (`version: 1.0.0`) diseñado originalmente para **GPT-4**. Con la llegada del nuevo modelo **Claude 3.5 Sonnet**, el equipo descubre que el prompt genera respuestas redundantes y que requiere incorporar una nueva variable obligatoria: `{TIPO_DE_CAMBIO}`.

### Tarea:
1. **Modelar el Flujo de Aprobación**: Describe en 3 o 4 pasos cómo se procesaría esta solicitud de cambio en el equipo de Auctoritas, especificando qué hace el *Editor*, qué hace el *Curador* y qué estados atraviesa el prompt (ej. Borrador, En Revisión, Aprobado).
2. **Redactar la Cabecera de Control de Versiones**:
   - Define el nuevo número de versión apropiado según las reglas de versionado semántico para prompts.
   - Crea un registro de cambios (**Changelog**) que documente el cambio, el autor, la fecha y la justificación.
3. **Plan de Mitigación de Riesgos**: Define cómo mitigarías los siguientes dos riesgos asociados:
   - **Riesgo A (Inconsistencia entre modelos)**: El prompt funciona excelente en Claude 3.5 Sonnet pero falla en GPT-4.
   - **Riesgo B (Baja adopción)**: Los analistas financieros siguen copiando de sus notas locales el prompt versión 1.0.0 en lugar de usar la nueva plantilla 1.1.0 del catálogo.

---

## 📥 Plantilla de Entrega

Crea el archivo `ejercicios/respuestas/ejercicio5_solucion.md` y estructura tu entrega de esta forma:

```markdown
# Solución Ejercicio 5

## 1. Flujo de Aprobación de Auctoritas
- Paso 1: ...
- Paso 2: ...
- Paso 3: ...

## 2. Metadatos de la Versión Actualizada y Changelog
```yaml
name: "Análisis Financiero"
version: [Indica la nueva versión]
last_updated: "2026-05-29"
compatible_models:
  - "Claude 3.5 Sonnet"
changelog:
  - version: "[Nueva Versión]"
    date: "2026-05-29"
    author: "Ing. de Prompts (Editor)"
    changes:
      - "Agregada la variable {TIPO_DE_CAMBIO}..."
      - "Optimizado el comportamiento para..."
  - version: "1.0.0"
    date: "2026-01-15"
    author: "Diseñador Original"
    changes:
      - "Lanzamiento inicial para GPT-4."
```

## 3. Mitigación de Riesgos
- **Mitigación para Inconsistencia entre Modelos**: ...
- **Mitigación para Baja Adopción**: ...
```
