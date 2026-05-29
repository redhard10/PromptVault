# Ejercicio 3: Plantillas con Variables y Placeholders

## Contexto Teórico
El uso de variables en los prompts es una de las mejores prácticas para convertirlos en herramientas altamente reutilizables. Un prompt estático obliga al usuario a reescribir la lógica cada vez que cambian los datos de entrada, lo cual introduce riesgos de consistencia.
Para parametrizar prompts, se utilizan **placeholders** (marcadores de posición) con la sintaxis `{VARIABLE_NAME}`.
Una buena documentación de variables debe incluir:
- **Nombre de la Variable**: En mayúsculas y serpiente/guion bajo para máxima visibilidad (ej. `{IDIOMA_DESTINO}`).
- **Tipo de Dato**: Texto, Número, Lista, Código, etc.
- **Descripción**: Qué representa la variable.
- **Valores de ejemplo**: Entradas válidas para guiar al usuario.

---

## 🎯 Instrucciones de la Tarea

Se te presenta un prompt estático que un equipo financiero utiliza diariamente para analizar balances financieros. Actualmente, copian, pegan y modifican manualmente el texto en ChatGPT, lo que produce reportes inconsistentes.

### Prompt Estático Original:
> "Quiero que analices el balance general de la empresa Tesla correspondiente al Q3 de 2025. Presta especial atención al ratio de liquidez corriente y al nivel de endeudamiento. Escribe una conclusión de máximo 3 párrafos en un tono formal y técnico, dirigida al Director de Finanzas."

### Tarea:
1. **Identifica y extrae las variables**: ¿Qué elementos cambian cada vez que se quiere analizar una empresa o un periodo diferente?
2. **Crea la Plantilla Reutilizable**: Reescribe el prompt utilizando placeholders en el formato `{PLACEHOLDER}`.
3. **Documenta las Variables**: Crea una tabla o lista estructurada detallando para cada variable: su Nombre, Tipo, Descripción y Ejemplo.
4. **Define una Guía de Validación**: Escribe una instrucción dentro del prompt que le indique al modelo qué hacer si el usuario ingresa un valor inválido o vacío en alguna de las variables.

---

## 📥 Plantilla de Entrega

Crea el archivo `ejercicios/respuestas/ejercicio3_solucion.md` y estructura tu entrega de esta forma:

```markdown
# Solución Ejercicio 3

## 1. Plantilla de Prompt Reutilizable
"..."

## 2. Tabla de Documentación de Variables
| Variable | Tipo | Descripción | Ejemplo de Entrada |
| :--- | :--- | :--- | :--- |
| `EMPRESA` | Texto | Nombre de la compañía a analizar | "Tesla Inc." |
| ... | ... | ... | ... |

## 3. Instrucción de Manejo de Errores e Invalidaciones
(Describe cómo integraste en la plantilla la instrucción para que el LLM gestione datos faltantes o incorrectos).
```
