import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write
import requests
import json
import base64

# Configuración de la API de Groq
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MODEL = "llama3-8b-8192"

# -----------------------
# Función para inicializar la API Key
# -----------------------
def inicializar_api_key():
    # Usar un identificador único para la clave almacenada
    st.sidebar.title("Configuración API")
    if "api_key_stored" not in st.session_state:
        # Inicializa el valor en el estado de la sesión solo una vez
        st.session_state["api_key_stored"] = ""

    # Utiliza una clave diferente para cada text_input
    if not st.session_state["api_key_stored"]:
        st.session_state["api_key_stored"] = st.sidebar.text_input(
            "Ingresa tu API Key de Groq:",
            type="password",
            key="unique_sidebar_api_key"  # Clave única estática para este único input
        )

    # Verificar si la clave fue ingresada
    if not st.session_state["api_key_stored"]:
        st.sidebar.warning("Por favor, ingresa una API Key válida para continuar.")
    return st.session_state["api_key_stored"]



# -----------------------
# Función para configurar los encabezados de las solicitudes
# -----------------------
def configurar_headers(api_key):
    return {
        'Authorization': f'Bearer {api_key}'
    }

# -----------------------
# Funciones mejoradas para Function Calling
# -----------------------
def obtener_clima(ciudad):
    headers = configurar_headers(inicializar_api_key())
    url = f"{GROQ_BASE_URL}/chat/completions"
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": f"En español: Describe el clima actual y agrega información relevante sobre {ciudad}."}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error al obtener el clima: {e}"

def calcular_ruta(origen, destino, modo):
    headers = configurar_headers(inicializar_api_key())
    url = f"{GROQ_BASE_URL}/chat/completions"
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": f"En español: Calcula la mejor ruta desde {origen} hasta {destino} usando {modo} y describe puntos de interés en el camino."}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error al calcular la ruta: {e}"

def recomendar_tours(ciudad):
    headers = configurar_headers(inicializar_api_key())
    url = f"{GROQ_BASE_URL}/chat/completions"
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": f" En español: Recomienda los mejores tours en {ciudad} y agrega detalles visuales relevantes si es posible."}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error al recomendar tours: {e}"

# -----------------------
# Función para grabar audio desde el micrófono
# -----------------------
def grabar_audio(duracion=10, frecuencia_muestreo=16000):
    try:
        st.info("Grabando audio...")
        audio = sd.rec(int(duracion * frecuencia_muestreo), samplerate=frecuencia_muestreo, channels=1, dtype='int16')
        sd.wait()
        st.success("Grabación completada")

        # Guardar el audio en formato wav
        archivo_audio = "audio.wav"
        write(archivo_audio, frecuencia_muestreo, audio)
        return archivo_audio
    except Exception as e:
        st.error(f"Error al grabar audio: {e}")
        return None

# Transcribir audio con Groq
def transcribir_audio(archivo_audio, headers):
    try:
        url = f"{GROQ_BASE_URL}/audio/transcriptions"
        files = {
            'file': (archivo_audio, open(archivo_audio, 'rb'), 'audio/wav')
        }
        data = {
            'model': 'whisper-large-v3-turbo',
            'language': 'es'
        }
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        result = response.json()
        return result['text']
    except requests.exceptions.RequestException as e:
        st.error(f"Error en la transcripción: {e}")
        return None

# -----------------------
# Procesar comandos con Function Calling en Groq
# -----------------------
def procesar_comando_groq(comando, headers):
    try:
        messages = [
            {"role": "system", "content": "Eres un asistente que puede realizar acciones específicas llamando funciones predefinidas."},
            {"role": "user", "content": comando}
        ]
        functions = [
            {
                "name": "obtener_clima",
                "description": "Obtiene el clima de una ciudad.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ciudad": {"type": "string", "description": "El nombre de la ciudad"}
                    },
                    "required": ["ciudad"]
                },
            },
            {
                "name": "calcular_ruta",
                "description": "Calcula la ruta entre dos ubicaciones.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "origen": {"type": "string", "description": "Punto de partida"},
                        "destino": {"type": "string", "description": "Punto de destino"},
                        "modo": {"type": "string", "description": "Modo de transporte (a pie, en automóvil, etc.)"}
                    },
                    "required": ["origen", "destino", "modo"]
                },
            },
            {
                "name": "recomendar_tours",
                "description": "Recomienda tours en una ciudad.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ciudad": {"type": "string", "description": "El nombre de la ciudad"}
                    },
                    "required": ["ciudad"]
                },
            },
        ]
        payload = {
            "model": MODEL,
            "messages": messages,
            "functions": functions,
            "function_call": "auto"
        }
        response = requests.post(f"{GROQ_BASE_URL}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        message = result['choices'][0]['message']
        if 'function_call' in message:
            function_name = message['function_call']['name']
            arguments = json.loads(message['function_call']['arguments'])  # Convertir a diccionario
            if function_name == 'obtener_clima':
                return obtener_clima(**arguments)
            elif function_name == 'calcular_ruta':
                return calcular_ruta(**arguments)
            elif function_name == 'recomendar_tours':
                return recomendar_tours(**arguments)
        else:
            return message['content']
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")
    return None

# -----------------------
# Interfaz con Streamlit
# -----------------------
def main():
    st.title("Asistente de Viaje con Function Calling y Groq")
    # Configurar API Key
    api_key = inicializar_api_key()
    if not api_key:
        return

    headers = configurar_headers(api_key)
    if st.button("Grabar Comando de Voz", key="grabar_audio_btn"):
        archivo_audio = grabar_audio(duracion=10)
        if archivo_audio:
            comando = transcribir_audio(archivo_audio, headers)
            if comando:
                st.write(f"Comando transcrito: {comando}")
                respuesta = procesar_comando_groq(comando, headers)
                if respuesta:
                    st.write(f"Respuesta: {respuesta}")
                else:
                    st.error("No se pudo procesar el comando.")
            else:
                st.error("No se pudo transcribir el audio.")

if __name__ == "__main__":
    main()
