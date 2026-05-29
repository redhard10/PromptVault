#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest
import json
import tempfile
import re

# Añadir el directorio raíz al path de importación
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from scripts.compile_prompts import parse_yaml_frontmatter, compile_file
except ImportError:
    print("[-] Error: No se pudo importar compile_prompts. Asegúrate de ejecutar este test desde el directorio raíz.")
    sys.exit(1)

class TestPromptRepository(unittest.TestCase):
    
    def setUp(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(self.script_dir)
        
    def test_directory_structure(self):
        """Verifica que todos los archivos esenciales del repositorio estén presentes."""
        expected_files = [
            "README.md",
            "index.html",
            "scripts/compile_prompts.py",
            "ejercicios/ejercicio1_taxonomia.md",
            "ejercicios/ejercicio2_formatos.md",
            "ejercicios/ejercicio3_variables.md",
            "ejercicios/ejercicio4_metaprompting.md",
            "ejercicios/ejercicio5_gobernanza.md",
            "libreria/marketing/redes_sociales/creador_hilos.md",
            "libreria/soporte/atencion_cliente/respuesta_empatica.md"
        ]
        
        for rel_path in expected_files:
            abs_path = os.path.join(self.project_root, rel_path.replace('/', os.sep))
            self.assertTrue(os.path.exists(abs_path), f"Falta el archivo requerido: {rel_path}")

    def test_frontmatter_parser(self):
        """Prueba unitaria del parser de YAML Frontmatter incorporado en compile_prompts.py."""
        yaml_content = """
        name: "Test Prompt"
        version: "1.2.0"
        description: "Un caso de prueba de ejemplo"
        compatible_models:
          - "gpt-4o"
          - "claude-3-5"
        variables:
          - "variable1"
          - "variable2"
        rag_context: false
        tags: ["test", "unittest"]
        numeric_val: 42
        """
        
        metadata = parse_yaml_frontmatter(yaml_content)
        
        self.assertEqual(metadata.get("name"), "Test Prompt")
        self.assertEqual(metadata.get("version"), "1.2.0")
        self.assertEqual(metadata.get("description"), "Un caso de prueba de ejemplo")
        self.assertEqual(metadata.get("compatible_models"), ["gpt-4o", "claude-3-5"])
        self.assertEqual(metadata.get("variables"), ["variable1", "variable2"])
        self.assertEqual(metadata.get("rag_context"), False)
        self.assertEqual(metadata.get("tags"), ["test", "unittest"])
        self.assertEqual(metadata.get("numeric_val"), 42)

    def test_compile_integration(self):
        """Verifica la compilación de extremo a extremo de un archivo Markdown a JSON."""
        # Crear un archivo markdown temporal
        with tempfile.NamedTemporaryFile(suffix='.md', mode='w+', delete=False, encoding='utf-8') as temp_md:
            temp_md.write("""---
name: "Temp Prompt"
version: "1.0.0"
description: "Temporal"
compatible_models:
  - "claude-3"
variables:
  - "temp_var"
rag_context: true
tags:
  - "temp"
---
Hola {temp_var}, esto es una plantilla.""")
            temp_md_path = temp_md.name
            
        try:
            # Ejecutar compilación
            success = compile_file(temp_md_path)
            self.assertTrue(success, "La compilación del archivo falló.")
            
            # Verificar existencia del JSON hermano
            json_path = os.path.splitext(temp_md_path)[0] + '.json'
            self.assertTrue(os.path.exists(json_path), "El archivo JSON compilado no fue creado.")
            
            # Verificar contenidos del JSON
            with open(json_path, 'r', encoding='utf-8') as fj:
                data = json.load(fj)
                
            self.assertEqual(data.get("name"), "Temp Prompt")
            self.assertEqual(data.get("version"), "1.0.0")
            self.assertEqual(data.get("prompt_text"), "Hola {temp_var}, esto es una plantilla.")
            self.assertEqual(data.get("rag_context"), True)
            self.assertEqual(data.get("variables"), ["temp_var"])
            
            # Limpiar archivo JSON temporal
            os.remove(json_path)
        finally:
            # Limpiar archivo MD temporal
            os.remove(temp_md_path)

    def test_author_attribution_and_copyright(self):
        """Asegura que el proyecto mencione la autoría de Gabriel Sessa y la licencia GPL, y no tenga copyright tradicional."""
        # 1. Comprobación de index.html
        html_path = os.path.join(self.project_root, "index.html")
        self.assertTrue(os.path.exists(html_path))
        
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        # Comprobar menciones de autoría y proyecto
        self.assertIn("Gabriel Sessa", html_content, "index.html debe mencionar al autor 'Gabriel Sessa'")
        self.assertIn("PromptVault", html_content, "index.html debe mencionar el nombre del proyecto 'PromptVault'")
        self.assertIn("GPL", html_content, "index.html debe mencionar la licencia GPL")
        
        # Comprobar copyright: no debe tener © ni "Copyright"
        self.assertNotIn("©", html_content, "index.html no debe tener símbolos de copyright ©")
        self.assertNotIn("Copyright", html_content, "index.html no debe tener referencias a Copyright")

        # 2. Comprobación de README.md
        readme_path = os.path.join(self.project_root, "README.md")
        self.assertTrue(os.path.exists(readme_path))
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
            
        self.assertIn("Gabriel Sessa", readme_content, "README.md debe mencionar al autor 'Gabriel Sessa'")
        self.assertIn("PromptVault", readme_content, "README.md debe mencionar el nombre del proyecto 'PromptVault'")
        self.assertIn("GPL", readme_content, "README.md debe mencionar la licencia GPL")
        self.assertNotIn("©", readme_content, "README.md no debe tener símbolos de copyright ©")
        self.assertNotIn("Copyright", readme_content, "README.md no debe tener referencias a Copyright")


class TestPromptDatabaseAndAPI(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        import server
        cls.server_mod = server
        
        # Respaldar base de datos y puerto originales
        cls.orig_db = server.DB_FILE
        cls.orig_port = server.PORT
        
        # Base de datos temporal
        cls.temp_db_fd, cls.temp_db_path = tempfile.mkstemp(suffix='.db')
        os.close(cls.temp_db_fd)
        server.DB_FILE = cls.temp_db_path
        
        # Inicializar y poblar base de datos de pruebas
        server.init_db()
        
        # Levantar servidor en hilo de fondo
        import socketserver
        socketserver.TCPServer.allow_reuse_address = True
        cls.httpd = socketserver.TCPServer(("", 0), server.PromptRequestHandler)
        server.PORT = cls.httpd.server_address[1]  # Asignar puerto libre de forma dinámica
        
        import threading
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        
    @classmethod
    def tearDownClass(cls):
        # Apagar servidor
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.server_thread.join()
        
        # Eliminar archivo de base de datos temporal
        if os.path.exists(cls.temp_db_path):
            try:
                os.remove(cls.temp_db_path)
            except Exception as e:
                print(f"[WARNING] No se pudo borrar el archivo temporal de base de datos: {e}")
                
        # Restaurar variables globales de server.py
        cls.server_mod.DB_FILE = cls.orig_db
        cls.server_mod.PORT = cls.orig_port
        
    def setUp(self):
        # Limpiar base de datos y volver a sembrar para garantizar aislamiento entre pruebas
        import sqlite3
        import server
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS prompts")
        conn.commit()
        conn.close()
        server.init_db()

    def test_database_initialization(self):
        """Verifica que la base de datos se crea correctamente y contiene los registros semilla."""
        import sqlite3
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, version FROM prompts")
        rows = cursor.fetchall()
        conn.close()
        
        # Verificar que hay 2 prompts semilla
        self.assertEqual(len(rows), 2)
        ids = [row[0] for row in rows]
        self.assertIn("creador_hilos", ids)
        self.assertIn("respuesta_empatica", ids)
        
    def test_api_get_prompts(self):
        """Verifica el endpoint GET /api/prompts y sus cabeceras CORS."""
        import urllib.request
        url = f"http://localhost:{self.server_mod.PORT}/api/prompts"
        req = urllib.request.Request(url)
        
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            headers = response.info()
            
            # Verificar cabeceras CORS
            self.assertEqual(headers.get('Access-Control-Allow-Origin'), '*')
            self.assertEqual(headers.get('Content-Type'), 'application/json; charset=utf-8')
            
            # Leer y decodificar cuerpo
            body = response.read().decode('utf-8')
            data = json.loads(body)
            
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['id'], 'creador_hilos')
            self.assertEqual(data[1]['id'], 'respuesta_empatica')
            self.assertTrue(isinstance(data[0]['variables'], list))
            self.assertTrue(isinstance(data[0]['tags'], list))
            
    def test_api_post_prompt_and_evolution(self):
        """Verifica el guardado y la evolución SemVer a través de POST /api/prompts."""
        import urllib.request
        import sqlite3
        url = f"http://localhost:{self.server_mod.PORT}/api/prompts"
        
        # 1. Crear nuevo prompt
        new_prompt = {
            "id": "asistente_redaccion",
            "name": "Asistente de Redacción Profesional",
            "version": "1.0.0",
            "description": "Corrige estilo y ortografía.",
            "compatible_models": ["GPT-4o"],
            "variables": ["texto", "estilo"],
            "rag_context": False,
            "tax": "escritura/redaccion",
            "tags": ["escritura", "correccion"],
            "prompt_text": "Corrige el siguiente texto: {texto} usando un estilo {estilo}.",
            "status": "borrador",
            "yaml_frontmatter": "name: \"Asistente de Redacción Profesional\"\nversion: \"1.0.0\""
        }
        
        req_data = json.dumps(new_prompt).encode('utf-8')
        req = urllib.request.Request(url, data=req_data, headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            body = response.read().decode('utf-8')
            res_data = json.loads(body)
            self.assertTrue(res_data.get("success"))
            
        # Verificar que se insertó en SQLite
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, version, variables, status FROM prompts WHERE id = ?", ("asistente_redaccion",))
        row = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "Asistente de Redacción Profesional")
        self.assertEqual(row[1], "1.0.0")
        self.assertEqual(json.loads(row[2]), ["texto", "estilo"])
        self.assertEqual(row[3], "borrador")
        
        # 2. Evolucionar prompt (POST para actualizar mismo ID con nueva versión y estado)
        evolved_prompt = new_prompt.copy()
        evolved_prompt["version"] = "1.1.0"
        evolved_prompt["prompt_text"] = "Corrige el siguiente texto: {texto} usando estilo {estilo} y formato markdown."
        evolved_prompt["variables"] = ["texto", "estilo", "formato"]
        evolved_prompt["status"] = "produccion"
        
        req_data_ev = json.dumps(evolved_prompt).encode('utf-8')
        req_ev = urllib.request.Request(url, data=req_data_ev, headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(req_ev) as response:
            self.assertEqual(response.status, 200)
            body = response.read().decode('utf-8')
            res_data = json.loads(body)
            self.assertTrue(res_data.get("success"))
            
        # Verificar en DB que se actualizó (obteniendo la versión más reciente)
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT version, prompt_text, variables, status FROM prompts WHERE id = ? ORDER BY version DESC", ("asistente_redaccion",))
        row = cursor.fetchone()
        
        # Verificar que coexisten ambas versiones
        cursor.execute("SELECT COUNT(*) FROM prompts WHERE id = ?", ("asistente_redaccion",))
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(row[0], "1.1.0")
        self.assertIn("formato markdown", row[1])
        self.assertEqual(json.loads(row[2]), ["texto", "estilo", "formato"])
        self.assertEqual(row[3], "produccion")
        self.assertEqual(count, 2, "Deberían coexistir 2 versiones del prompt en la base de datos")
        
    def test_api_delete_prompt(self):
        """Verifica la eliminación de prompts usando DELETE /api/prompts."""
        import urllib.request
        import sqlite3
        # Insertar un prompt temporal a eliminar
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO prompts (id, name, version, prompt_text) VALUES (?, ?, ?, ?)",
            ("a_eliminar", "Temporal", "0.1.0", "Prompt temporal")
        )
        conn.commit()
        conn.close()
        
        # Verificar existencia inicial
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM prompts WHERE id = ?", ("a_eliminar",))
        count_before = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(count_before, 1)
        
        # Hacer petición DELETE
        url = f"http://localhost:{self.server_mod.PORT}/api/prompts?id=a_eliminar"
        req = urllib.request.Request(url, method="DELETE")
        
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            body = response.read().decode('utf-8')
            res_data = json.loads(body)
            self.assertTrue(res_data.get("success"))
            
        # Verificar eliminación final
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM prompts WHERE id = ?", ("a_eliminar",))
        count_after = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(count_after, 0)
        
    def test_api_options_preflight(self):
        """Verifica las cabeceras CORS en una petición OPTIONS (CORS preflight)."""
        import urllib.request
        url = f"http://localhost:{self.server_mod.PORT}/api/prompts"
        req = urllib.request.Request(url, method="OPTIONS")
        
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            headers = response.info()
            self.assertEqual(headers.get('Access-Control-Allow-Origin'), '*')
            self.assertEqual(headers.get('Access-Control-Allow-Methods'), 'GET, POST, DELETE, OPTIONS')
            self.assertEqual(headers.get('Access-Control-Allow-Headers'), 'Content-Type')
            
    def test_api_invalid_post_missing_fields(self):
        """Verifica que el servidor retorne un 400 Bad Request si faltan campos obligatorios."""
        import urllib.request
        import urllib.error
        url = f"http://localhost:{self.server_mod.PORT}/api/prompts"
        
        # Petición incompleta (falta prompt_text)
        incomplete_prompt = {
            "id": "incompleto",
            "name": "Prompt sin texto",
            "version": "1.0.0"
        }
        
        req_data = json.dumps(incomplete_prompt).encode('utf-8')
        req = urllib.request.Request(url, data=req_data, headers={'Content-Type': 'application/json'})
        
        # Capturamos el error HTTP 400
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen(req)
            
        self.assertEqual(cm.exception.code, 400)


if __name__ == '__main__':
    print("==================================================")
    print("[INFO] Iniciando set de pruebas automatizadas...")
    print("==================================================")
    
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPromptRepository))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPromptDatabaseAndAPI))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("==================================================")
    if result.wasSuccessful():
        print("[OK] ¡Todas las pruebas pasaron exitosamente!")
        sys.exit(0)
    else:
        print("[-] Falló alguna de las pruebas en el set.")
        sys.exit(1)
