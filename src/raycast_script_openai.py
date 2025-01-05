#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Mejorar_Texto_OpenAI
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖

# Documentation:
# @raycast.description Script para llamar a LLM ligero para arreglar textos
# @raycast.author Alejandro Tinto
# @raycast.authorURL https://www.linkedin.com/in/alejandro-tinto/


import subprocess
import requests
import os
import sys

OPENAI_API_KEY = "TU-API-DE-OPENAI"

# Usa el modelo que quieras
MODEL = "gpt-4o-mini"

# Prompt del sistema para corregir ortografía
SYSTEM_PROMPT = """
Eres un asistente de IA cuya responsabilidad principal es tomar una selección de texto y corregir su ortografía. Analizas meticulosamente el texto para identificar cualquier error ortográfico y corregirlo. Tu rol requiere atención al detalle y precisión para asegurar que el texto final esté libre de errores ortográficos.
Sigue estos pasos:
1. Lee cuidadosamente el texto proporcionado.
2. Identifica cualquier palabra que esté mal escrita.
3. Corrige la ortografía de las palabras identificadas.
4. Revisa el texto corregido para asegurar que no queden errores ortográficos.
Instrucciones de salida:
- Solo produce el texto corregido en formato de texto plano.
- Proporciona la selección de texto corregida en un formato limpio y legible.
- No añadas nada más a la salida.
- Asegúrate de seguir TODAS estas instrucciones al crear tu salida.
"""

# URL del endpoint de completions de OpenAI
URL = "https://api.openai.com/v1/chat/completions"

# Cabeceras para la solicitud HTTP
HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}

def obtener_texto_seleccionado():
    try:
        # Copiar el texto seleccionado al portapapeles
        applescript = '''
        tell application "System Events"
            keystroke "c" using {command down}
        end tell
        '''
        subprocess.run(['osascript', '-e', applescript])
        texto = subprocess.check_output("pbpaste", universal_newlines=True)
        return texto.strip()
    except Exception as e:
        print(f"Error al obtener el texto seleccionado: {e}")
        sys.exit(1)

def corregir_texto(texto):
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": texto},
        ],
        "temperature": 0,
        "max_tokens": 1024,
    }
    try:
        response = requests.post(URL, headers=HEADERS, json=data)
        response.raise_for_status()
        contenido = response.json()
        return contenido["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud a OpenAI: {e}")
        sys.exit(1)
    except (KeyError, IndexError):
        print("Error: Respuesta inesperada de la API de OpenAI.")
        sys.exit(1)

def poner_texto_portapapeles(texto):
    try:
        proceso = subprocess.Popen(
            "pbcopy", env={"LANG": "en_US.UTF-8"}, stdin=subprocess.PIPE, close_fds=True
        )
        proceso.communicate(texto.encode('utf-8'))
    except Exception as e:
        print(f"Error al poner texto en el portapapeles: {e}")
        sys.exit(1)

def pegar_texto():
    try:
        applescript = '''
            tell application "System Events"
                keystroke "v" using command down
            end tell
        '''
        subprocess.run(['osascript', '-e', applescript])
    except Exception as e:
        print(f"Error al simular pegar texto: {e}")
        sys.exit(1)
        
def copiar_seleccion():
    try:
        applescript = '''
            tell application "System Events"
                keystroke "c" using command down
            end tell
        '''
        subprocess.run(['osascript', '-e', applescript])
    except Exception as e:
        print(f"Error al simular copiar la selección: {e}")
        sys.exit(1)

def main():
    copiar_seleccion()
    texto_original = obtener_texto_seleccionado()
    if not texto_original:
        print("No se ha detectado texto en el portapapeles.")
        sys.exit(1)
    
    texto_corregido = corregir_texto(texto_original)
    poner_texto_portapapeles(texto_corregido)
    print("Texto corregido!!!")
    pegar_texto()

if __name__ == "__main__":
    main()

