#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json

def parse_yaml_frontmatter(yaml_str):
    """
    Parsea de forma básica un bloque YAML de metadatos (Frontmatter).
    Diseñado para funcionar sin dependencias externas como PyYAML.
    """
    metadata = {}
    lines = yaml_str.strip().split('\n')
    current_key = None
    
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue
        
        # Ignorar comentarios
        if stripped_line.startswith('#'):
            continue
            
        # Caso de elemento de lista YAML (ej.  - "variable")
        if stripped_line.startswith('-') and current_key:
            val = stripped_line[1:].strip().strip('"').strip("'")
            if current_key not in metadata:
                metadata[current_key] = []
            elif not isinstance(metadata[current_key], list):
                metadata[current_key] = [metadata[current_key]]
            metadata[current_key].append(val)
            continue
            
        # Par de clave-valor (ej. name: "Creador de Hilos")
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip()
            val = parts[1].strip()
            
            # Caso de lista inline (ej. tags: ["a", "b"])
            if val.startswith('[') and val.endswith(']'):
                items = [item.strip().strip('"').strip("'") for item in val[1:-1].split(',')]
                metadata[key] = items
                current_key = key
            # Caso de lista multilinea que inicia
            elif not val:
                metadata[key] = []
                current_key = key
            # Caso valor normal
            else:
                # Conversión de tipos
                if val.lower() == 'true':
                    val = True
                elif val.lower() == 'false':
                    val = False
                elif val.isdigit():
                    val = int(val)
                else:
                    val = val.strip('"').strip("'")
                metadata[key] = val
                current_key = key
                
    return metadata

def compile_file(md_path):
    """
    Lee un archivo Markdown, separa el Frontmatter del Prompt y lo escribe en formato JSON.
    """
    print(f"Procesando: {os.path.basename(md_path)}...")
    
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # El frontmatter se encuentra entre delimitadores '---'
        # Usamos expresión regular para extraer el contenido entre los primeros '---'
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        
        if not match:
            print(f"[-] Error: El archivo {md_path} no tiene un formato válido con delimitadores '---' al inicio.")
            return False
            
        yaml_content = match.group(1)
        prompt_text = match.group(2).strip()
        
        metadata = parse_yaml_frontmatter(yaml_content)
        
        # Agregamos el texto del prompt propiamente dicho
        metadata['prompt_text'] = prompt_text
        
        # Generar ruta del archivo JSON correspondiente
        json_path = os.path.splitext(md_path)[0] + '.json'
        
        with open(json_path, 'w', encoding='utf-8') as f_json:
            json.dump(metadata, f_json, indent=2, ensure_ascii=False)
            
        print(f"[OK] Compilado con éxito: {os.path.basename(json_path)}")
        return True
        
    except Exception as e:
        print(f"[-] Error al procesar {md_path}: {str(e)}")
        return False

def main():
    # La carpeta libreria está en el mismo directorio principal del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    library_dir = os.path.join(project_root, 'libreria')
    
    if not os.path.exists(library_dir):
        print(f"[-] La carpeta de biblioteca no existe en {library_dir}")
        return
        
    compiled_count = 0
    error_count = 0
    
    print("==================================================")
    print("[INFO] Iniciando compilación de biblioteca de prompts...")
    print("==================================================")
    
    for root, dirs, files in os.walk(library_dir):
        for file in files:
            if file.endswith('.md'):
                md_path = os.path.join(root, file)
                success = compile_file(md_path)
                if success:
                    compiled_count += 1
                else:
                    error_count += 1
                    
    print("==================================================")
    print(f"[INFO] Compilación finalizada. Éxitos: {compiled_count}, Errores: {error_count}")
    print("==================================================")

if __name__ == '__main__':
    main()
