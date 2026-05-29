# 🔐 PromptVault — Gestión Inteligente de Librerías de Prompts

<div align="center">

![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow.svg)
![HTML](https://img.shields.io/badge/Frontend-HTML%20%2B%20JS-orange.svg)
![SQLite](https://img.shields.io/badge/DB-SQLite-lightgrey.svg)
![Author](https://img.shields.io/badge/Autor-Gabriel%20Sessa-purple.svg)

*La bóveda inteligente para diseñar, versionar, auditar y gobernar tu biblioteca de prompts con IA Generativa.*

</div>

---

## 🚀 Inicio Rápido (Para Alumnos)

> **Prerrequisitos**: Python 3.10 o superior instalado. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).

### Opción A — Con servidor local (recomendada, persiste tus prompts en SQLite)

```bash
# 1. Clona el repositorio en tu computadora
git clone https://github.com/redhard10/PracticaRepositoriosPrompting.git

# 2. Ingresa a la carpeta del proyecto
cd PracticaRepositoriosPrompting

# 3. Lanza el servidor local
python server.py
```

Luego abre tu navegador en **[http://localhost:8000](http://localhost:8000)** 🎉

### Opción B — Sin servidor (modo offline, guarda en el navegador)

Simplemente descarga el repositorio como ZIP desde GitHub y **abre el archivo `index.html`** con doble clic. Los datos se guardan automáticamente en el `localStorage` de tu navegador.

---

## 📌 Descripción del Proyecto

Este espacio de trabajo ha sido diseñado para la enseñanza práctica de **Ingeniería de Prompts y Gestión de Bibliotecas de IA Generativa**, siguiendo los principios del diseño estructurado de catálogos y técnicas avanzadas de **Meta-Prompting**.

### ¿Qué puedes hacer con esta plataforma?

| Módulo | Descripción |
|--------|-------------|
| 📚 **Biblioteca de Prompts** | Catálogo visual de plantillas semilla con filtros por etiqueta y estado |
| 🧩 **Compilador de Variables** | Inyecta valores reales en los placeholders `{VARIABLE}` de forma interactiva |
| 🔄 **Conversor YAML/JSON** | Convierte prompts de formato humano (Markdown) a JSON estructurado para APIs |
| 📝 **Ejercicios Prácticos** | Resuelve y valida los 5 ejercicios del taller con retroalimentación inmediata |
| 🤖 **Asistente Meta-Prompt** | Genera prompts optimizados usando técnicas de orquestación y Chain of Thought |
| 🧠 **Evaluador de IA** | Audita tus prompts conectándose a Gemini, OpenAI u Ollama local |

---

## 📖 Fundamentos Teóricos

### 1. ¿Por qué una Biblioteca de Prompts?
Al igual que un restaurante de alta cocina confía en recetas estandarizadas y probadas en lugar de improvisar cada plato, una organización debe contar con un **catálogo de prompts validados**. Esto garantiza tres beneficios fundamentales:
* **Eficiencia**: Evita reinventar la rueda y reduce el tiempo de redacción de instrucciones a segundos.
* **Consistencia**: Asegura que las respuestas de los LLM mantengan la misma estructura, tono y calidad, independientemente de quién los ejecute.
* **Colaboración**: Permite compartir conocimiento y mejorar las instrucciones de forma colectiva en equipos de trabajo.

### 2. Los Pilares de Guadián (2025)

#### A. Estructura y Taxonomía Multidimensional
* **Ruta de Categoría**: Carpetas organizadas de forma lógica (ej. `marketing/redes_sociales/`).
* **Etiquetas Múltiples**: Permiten que un mismo prompt pertenezca a varios contextos sin duplicar el archivo.
* **Metadatos Estándar**: Cada prompt debe auto-documentarse incluyendo:
  - `name`, `version`, `description`, `compatible_models`, `variables`, `rag_context`, `tags`

#### B. El Doble Formato (Humano-Máquina)
* **Markdown + YAML Frontmatter**: Para que los humanos lean y editen fácilmente.
* **JSON**: Compilado automáticamente para ser consumido por APIs y orquestadores.

#### C. Gobernanza y Versionado Semántico (SemVer)
Los prompts son tratados como **artefactos de código** con historial de versiones:
* `Mayor.Menor.Parche` — Cada versión se preserva en la base de datos.
* Estados de ciclo de vida: **En Producción**, **En Revisión**, **Borrador**, **Deprecado**.
* Posibilidad de tener múltiples versiones activas simultáneamente.

---

## ⚡ Meta-Prompting

El **Meta-Prompting** es la técnica donde utilizamos el propio LLM como asistente de ingeniería para generar prompts más eficaces:
1. **Auto-meta Prompting**: Pedir al LLM que diseñe de forma autónoma el mejor prompt para una tarea.
2. **Orquestación**: Un "director de orquesta" descompone tareas complejas y delega a "expertos virtuales".
3. **Iteración en Bucle**: Evaluar y refinar el prompt hasta cumplir estándares de calidad.

---

## 🗂️ Estructura del Repositorio

```
PracticaRepositoriosPrompting/
│
├── index.html                  # 🖥️  Dashboard interactivo principal
├── server.py                   # 🐍  Servidor Python + API REST SQLite
├── manual_de_usuario.md        # 📖  Manual completo de la plataforma
├── README.md                   # 📄  Este archivo
├── LICENSE                     # ⚖️  Licencia GPL v3
├── .gitignore                  # 🚫  Archivos excluidos de Git
│
├── ejercicios/                 # 📝  Enunciados de los 5 ejercicios prácticos
│   ├── ejercicio1_taxonomia.md
│   ├── ejercicio2_formatos.md
│   ├── ejercicio3_variables.md
│   ├── ejercicio4_metaprompting.md
│   └── ejercicio5_gobernanza.md
│
├── libreria/                   # 📚  Prompts semilla en formato Markdown + YAML
│   ├── marketing/
│   └── soporte/
│
└── scripts/                    # ⚙️  Herramientas de automatización
    ├── compile_prompts.py      # Compila Markdown → JSON
    └── test_suite.py           # Suite de 10 pruebas automatizadas
```

> **Nota**: El archivo `prompts.db` (base de datos SQLite) se genera automáticamente al ejecutar `server.py` y **no está versionado en Git**.

---

## 🔧 Comandos Útiles

```bash
# Iniciar el servidor (crea prompts.db automáticamente)
python server.py

# Compilar prompts Markdown de la librería a JSON
python scripts/compile_prompts.py

# Ejecutar el set de pruebas automatizadas (10 tests)
python scripts/test_suite.py
```

### Usar el Evaluador de IA con Ollama (Local, sin costo)

```bash
# Windows: iniciar Ollama permitiendo conexiones desde el navegador
cmd /c "set OLLAMA_ORIGINS=* && ollama serve"
```

Luego en la app: pestaña **Evaluador IA** → selecciona **Ollama (Local)** → click **🔄 Cargar** para detectar tus modelos instalados.

---

## 📄 Licencia y Autoría

Este proyecto es software libre y de código abierto, distribuido bajo la **GNU General Public License v3**. Puedes redistribuirlo y/o modificarlo de forma gratuita bajo los términos de la misma.

* **Autor**: Gabriel Sessa
* **Email**: [gabriel.linux.ar@gmail.com](mailto:gabriel.linux.ar@gmail.com)
* **GitHub**: [github.com/redhard10](https://github.com/redhard10)
* **LinkedIn**: [linkedin.com/in/gabrielsessa](https://linkedin.com/in/gabrielsessa)
