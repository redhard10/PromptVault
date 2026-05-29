# Ejercicio 4: Meta-Prompting en Tres Etapas

## Contexto Teórico
El **Meta-prompting** consiste en utilizar un LLM como un "ingeniero de prompts" virtual. En lugar de escribir prompts detallados por nuestra cuenta, estructuramos una instrucción (meta-prompt) que le enseña al modelo cómo construir prompts de alta calidad para nosotros.

Trabajaremos con tres enfoques de meta-prompting:

1. **Auto-meta Prompting (Auto-generación)**: Una estructura única que le pide al modelo que analice una tarea compleja y redacte el prompt óptimo para resolverla, definiendo un rol de experto, restricciones de formato, y criterios de salida.
2. **Orquestación (Director y Expertos)**: Un meta-prompt que actúa como "Director" y descompone un problema en subtareas, simula las respuestas de expertos virtuales especializados en cada subtarea y consolida un consenso final.
3. **Iterativo en Bucle (Evaluador y Refinador)**: Un sistema interactivo donde el modelo evalúa la calidad de un prompt borrador mediante una rúbrica específica (ej. claridad, concisión, especificidad) y lo reescribe en ciclos hasta que alcance una calificación perfecta (10/10).

---

## 🎯 Instrucciones de la Tarea

Debes diseñar y documentar tres meta-prompts específicos para resolver la siguiente tarea compleja de negocio:
> **Tarea**: Analizar noticias financieras e identificar si contienen indicios de manipulación de mercado o información privilegiada, generando un informe de riesgo.

### Tarea A: Auto-meta Prompt
Escribe un meta-prompt diseñado para que, al ingresarlo en un LLM, este genere un **prompt de usuario final** optimizado para resolver la Tarea. 
* *Restricción*: El meta-prompt generado por ti debe obligar al LLM a incluir en su respuesta: el rol del experto, las instrucciones paso a paso, variables de entrada `{NOTICIA_FINANCIERA}` y una sección de auto-verificación en la salida.

### Tarea B: Prompt de Orquestación (Director de Expertos)
Diseña un prompt del tipo "Director de Orquesta" para evaluar la noticia. Este prompt debe:
* Indicar al LLM que simule un panel compuesto por tres expertos virtuales: un *Analista Financiero Senior*, un *Abogado Especialista en Regulación de Valores (SEC)*, y un *Experto en Análisis Forense de Texto*.
* Indicar el proceso donde cada uno de los expertos da su veredicto de forma secuencial.
* Incluir una etapa de debate e integración final donde el "Director" unifique los tres análisis y resuelva contradicciones.

### Tarea C: Bucle de Refinamiento Iterativo
Escribe un prompt evaluador que reciba un prompt borrador, aplique una rúbrica de 3 puntos (Claridad de Restricciones, Manejo de Casos de Borde, Estructura de Salida) y proporcione una versión mejorada. Este evaluador debe continuar el bucle hasta dar una puntuación detallada de 10/10 en cada aspecto.

---

## 📥 Plantilla de Entrega

Crea el archivo `ejercicios/respuestas/ejercicio4_solucion.md` con los tres meta-prompts terminados para que puedan ser copiados y ejecutados:

```markdown
# Solución Ejercicio 4

## 1. Meta-Prompt A: Auto-meta Prompting
```text
[Escribe aquí el meta-prompt. Ej. "Actúa como un Ingeniero de Prompts Experto. Diseña un prompt de sistema detallado para resolver la tarea de analizar noticias..."]
```

## 2. Meta-Prompt B: Orquestador (Director y Expertos)
```text
[Escribe aquí tu prompt orquestador de expertos virtuales]
```

## 3. Meta-Prompt C: Bucle de Refinamiento Iterativo
```text
[Escribe aquí tu prompt evaluador e iterador en base a rúbricas]
```
```
