#!/usr/bin/env python
# -*- coding: utf-8 -*-

import http.server
import socketserver
import json
import sqlite3
import os
import urllib.parse
import sys

PORT = 8000
DB_FILE = 'prompts.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    print("[INFO] Inicializando base de datos SQLite...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Migración de base de datos existente: detectar si la clave primaria es simple (id) y migrarla a compuesta (id, version)
    try:
        cursor.execute("PRAGMA table_info(prompts)")
        info = cursor.fetchall()
        if info:
            pk_count = sum(1 for col in info if col[5] > 0)
            if pk_count == 1:
                print("[INFO] Detectada clave primaria antigua. Migrando a clave primaria compuesta (id, version)...")
                # Renombrar tabla antigua
                cursor.execute("ALTER TABLE prompts RENAME TO prompts_old")
                # Crear nueva tabla con clave compuesta
                cursor.execute('''
                    CREATE TABLE prompts (
                        id TEXT,
                        name TEXT NOT NULL,
                        version TEXT NOT NULL,
                        description TEXT,
                        compatible_models TEXT,
                        variables TEXT,
                        rag_context INTEGER,
                        tax TEXT,
                        tags TEXT,
                        prompt_text TEXT NOT NULL,
                        yaml_frontmatter TEXT,
                        status TEXT DEFAULT 'produccion',
                        PRIMARY KEY (id, version)
                    )
                ''')
                # Copiar datos existentes
                cursor.execute('''
                    INSERT OR REPLACE INTO prompts (id, name, version, description, compatible_models, variables, rag_context, tax, tags, prompt_text, yaml_frontmatter, status)
                    SELECT id, name, version, description, compatible_models, variables, rag_context, tax, tags, prompt_text, yaml_frontmatter, status FROM prompts_old
                ''')
                # Eliminar tabla antigua
                cursor.execute("DROP TABLE prompts_old")
                conn.commit()
                print("[OK] Migración de base de datos finalizada con éxito.")
    except sqlite3.OperationalError:
        # La tabla no existe aún, se creará normalmente a continuación
        pass

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id TEXT,
            name TEXT NOT NULL,
            version TEXT NOT NULL,
            description TEXT,
            compatible_models TEXT,
            variables TEXT,
            rag_context INTEGER,
            tax TEXT,
            tags TEXT,
            prompt_text TEXT NOT NULL,
            yaml_frontmatter TEXT,
            status TEXT DEFAULT 'produccion',
            PRIMARY KEY (id, version)
        )
    ''')
    
    # Asegurar columna status por si acaso
    try:
        cursor.execute("ALTER TABLE prompts ADD COLUMN status TEXT DEFAULT 'produccion'")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    
    # Verificar si está vacía la base de datos
    cursor.execute('SELECT COUNT(*) FROM prompts')
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("[INFO] Base de datos vacía. Sembrando prompts semilla...")
        seeds = [
            {
                "id": "creador_hilos",
                "name": "Creador de Hilos de Contenido",
                "version": "1.0.0",
                "description": "Generador de hilos secuenciales atractivos para Twitter/X y LinkedIn a partir de un tema central.",
                "compatible_models": json.dumps(["Claude 3.5 Sonnet", "GPT-4o"], ensure_ascii=False),
                "variables": json.dumps(["tema", "canales", "tono", "n_tweets"], ensure_ascii=False),
                "rag_context": 0,
                "tax": "marketing/redes_sociales",
                "tags": json.dumps(["marketing", "redes_sociales", "copywriting", "hilos"], ensure_ascii=False),
                "prompt_text": "Eres un redactor creativo experto y estratega de marca personal en redes sociales. Tu tarea es redactar un hilo de contenido secuencial optimizado para los canales de {canales} basándote en la siguiente temática central: {tema}.\n\nSigue estas pautas estrictas al redactar el hilo:\n1. El número total de publicaciones del hilo debe ser exactamente de {n_tweets}.\n2. Adopta un tono {tono}.\n3. El primer tuit/post debe ser un \"gancho\" (hook) magnético que incite al lector a abrir el hilo, planteando una pregunta provocadora, una estadística sorprendente o un dolor común.\n4. Cada post intermedio del hilo debe aportar un valor práctico o una lección, utilizando un formato estructurado con viñetas cortas si es posible para facilitar la lectura.\n5. El post final del hilo debe incluir un llamado a la acción (CTA) claro, invitando a la audiencia a interactuar (comentar, compartir o dar me gusta).\n6. Respeta los límites de caracteres por red social (280 para Twitter, pero mantén un buen espacio en blanco).\n\nGenera el hilo numerando claramente cada sección: \"Post 1\", \"Post 2\", etc.",
                "yaml_frontmatter": "name: \"Creador de Hilos de Contenido\"\nversion: \"1.0.0\"\ndescription: \"Generador de hilos secuenciales atractivos para Twitter/X y LinkedIn a partir de un tema central.\"\ncompatible_models:\n  - \"Claude 3.5 Sonnet\"\n  - \"GPT-4o\"\nvariables:\n  - \"tema\"\n  - \"canales\"\n  - \"tono\"\n  - \"n_tweets\"\nrag_context: false\ntags:\n  - \"marketing\"\n  - \"redes_sociales\"\n  - \"copywriting\"\n  - \"hilos\"",
                "status": "produccion"
            },
            {
                "id": "respuesta_empatica",
                "name": "Respuesta Empática de Soporte",
                "version": "1.1.0",
                "description": "Plantilla para redactar respuestas de soporte técnico personalizadas, claras y empáticas para clientes frustrados.",
                "compatible_models": json.dumps(["Claude 3.5 Sonnet", "GPT-4o", "Llama-3-70b"], ensure_ascii=False),
                "variables": json.dumps(["producto", "cliente", "problema"], ensure_ascii=False),
                "rag_context": 0,
                "tax": "soporte/atencion_cliente",
                "tags": json.dumps(["soporte", "atencion_cliente", "empatia", "operaciones"], ensure_ascii=False),
                "prompt_text": "Eres un agente senior de soporte técnico para {producto}. Tu objetivo es redactar una respuesta profesional, empática y resolutiva dirigida a nuestro cliente {cliente}, quien está experimentando el siguiente problema: {problema}.\n\nEstructura tu respuesta exactamente en los siguientes pasos:\n1. **Saludo Personalizado y Validación del Sentimiento**: Saluda a {cliente} por su nombre. Expresa de forma genuina que comprendes su molestia y valida su frustración sin culpar a terceros.\n2. **Explicación del Problema**: Si el problema es común, describe brevemente por qué ocurre en términos sencillos.\n3. **Plan de Acción / Solución**: Proporciona de 2 a 4 pasos numerados y claros para resolver el problema o indica cuál es el siguiente paso que daremos desde el equipo técnico.\n4. **Cierre Amigable y Canal de Seguimiento**: Finaliza reiterando tu disposición a ayudar, utilizando un tono profesional y optimista.",
                "yaml_frontmatter": "name: \"Respuesta Empática de Soporte\"\nversion: \"1.1.0\"\ndescription: \"Plantilla para redactar respuestas de soporte técnico personalizadas, claras y empáticas para clientes frustrados.\"\ncompatible_models:\n  - \"Claude 3.5 Sonnet\"\n  - \"GPT-4o\"\n  - \"Llama-3-70b\"\nvariables:\n  - \"producto\"\n  - \"cliente\"\n  - \"problema\"\nrag_context: false\ntags:\n  - \"soporte\"\n  - \"atencion_cliente\"\n  - \"empatia\"\n  - \"operaciones\"",
                "status": "produccion"
            }
        ]
        
        for seed in seeds:
            cursor.execute('''
                INSERT INTO prompts (id, name, version, description, compatible_models, variables, rag_context, tax, tags, prompt_text, yaml_frontmatter, status)
                VALUES (:id, :name, :version, :description, :compatible_models, :variables, :rag_context, :tax, :tags, :prompt_text, :yaml_frontmatter, :status)
            ''', seed)
        conn.commit()
        print("[INFO] Siembra finalizada con éxito.")
    conn.close()


class PromptRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def send_json(self, data, status=200):
        response_bytes = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        # Responder a CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        if path == '/api/prompts':
            self.handle_get_prompts()
        elif path == '/' or path == '/index.html':
            self.path = '/index.html'
            return super().do_GET()
        else:
            # Servir archivo estático (SimpleHTTPRequestHandler resolverá la ruta)
            return super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        if path == '/api/prompts':
            self.handle_post_prompts()
        else:
            self.send_error(404, "Ruta de API no encontrada")

    def do_DELETE(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = urllib.parse.parse_qs(parsed_url.query)
        
        if path == '/api/prompts':
            self.handle_delete_prompts(query)
        else:
            self.send_error(404, "Ruta de API no encontrada")

    def handle_get_prompts(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM prompts')
            rows = cursor.fetchall()
            
            prompts = []
            for row in rows:
                p = dict(row)
                # Deserializar campos JSON
                try:
                    p['compatible_models'] = json.loads(p['compatible_models'])
                except:
                    p['compatible_models'] = []
                    
                try:
                    p['variables'] = json.loads(p['variables'])
                except:
                    p['variables'] = []
                    
                try:
                    p['tags'] = json.loads(p['tags'])
                except:
                    p['tags'] = []
                    
                p['rag_context'] = bool(p['rag_context'])
                prompts.append(p)
                
            conn.close()
            self.send_json(prompts)
        except Exception as e:
            self.send_json({"error": f"Error en base de datos: {str(e)}"}, 500)

    def handle_post_prompts(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(post_data)
            required = ['id', 'name', 'version', 'prompt_text']
            for r in required:
                if r not in data or not data[r]:
                    self.send_json({"error": f"Falta el campo obligatorio: '{r}'"}, 400)
                    return
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Serializar campos de lista
            compatible_models = data.get('compatible_models', [])
            if isinstance(compatible_models, list):
                compatible_models = json.dumps(compatible_models, ensure_ascii=False)
            
            variables = data.get('variables', [])
            if isinstance(variables, list):
                variables = json.dumps(variables, ensure_ascii=False)
                
            tags = data.get('tags', [])
            if isinstance(tags, list):
                tags = json.dumps(tags, ensure_ascii=False)
                
            rag_context = 1 if data.get('rag_context', False) else 0
            
            cursor.execute('''
                INSERT INTO prompts (id, name, version, description, compatible_models, variables, rag_context, tax, tags, prompt_text, yaml_frontmatter, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id, version) DO UPDATE SET
                    name=excluded.name,
                    description=excluded.description,
                    compatible_models=excluded.compatible_models,
                    variables=excluded.variables,
                    rag_context=excluded.rag_context,
                    tax=excluded.tax,
                    tags=excluded.tags,
                    prompt_text=excluded.prompt_text,
                    yaml_frontmatter=excluded.yaml_frontmatter,
                    status=excluded.status
            ''', (
                data['id'],
                data['name'],
                data['version'],
                data.get('description', ''),
                compatible_models,
                variables,
                rag_context,
                data.get('tax', 'general'),
                tags,
                data['prompt_text'],
                data.get('yaml_frontmatter', ''),
                data.get('status', 'produccion')
            ))
            
            conn.commit()
            conn.close()
            self.send_json({"success": True})
            print(f"[OK] Prompt '{data['name']}' (v{data['version']}) guardado en SQLite.")
        except Exception as e:
            self.send_json({"error": f"Error al procesar guardado: {str(e)}"}, 500)

    def handle_delete_prompts(self, query):
        p_ids = query.get('id', [])
        if not p_ids:
            self.send_json({"error": "Falta parámetro 'id'"}, 400)
            return
        
        p_id = p_ids[0]
        p_versions = query.get('version', [])
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            if p_versions:
                p_ver = p_versions[0]
                cursor.execute('DELETE FROM prompts WHERE id=? AND version=?', (p_id, p_ver))
                print(f"[OK] Prompt '{p_id}' versión '{p_ver}' eliminado de la base de datos.")
            else:
                cursor.execute('DELETE FROM prompts WHERE id=?', (p_id,))
                print(f"[OK] Todas las versiones del prompt '{p_id}' eliminadas de la base de datos.")
            conn.commit()
            conn.close()
            self.send_json({"success": True})
        except Exception as e:
            self.send_json({"error": str(e)}, 500)


def main():
    init_db()
    
    # Cambiar al directorio del proyecto para servir archivos estáticos correctamente
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    handler = PromptRequestHandler
    
    # Permitir reiniciar rápido el puerto sin esperar TIME_WAIT
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print("==================================================")
            print(f"[INFO] Servidor de Repositorio de Prompts Activo!")
            print(f"[INFO] Abre en tu navegador: http://localhost:{PORT}")
            print("==================================================")
            print("[INFO] Para apagar el servidor presiona Ctrl+C.")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Apagando el servidor local de prompts.")
        sys.exit(0)
    except Exception as e:
        print(f"[-] Error al iniciar el servidor: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
