# Asistente de Viaje con Function Calling y Groq

Este proyecto implementa un asistente de viaje basado en **Streamlit** que utiliza la API de Groq para procesar comandos, transcribir audio y proporcionar funciones mejoradas como obtener información del clima, calcular rutas, y recomendar tours.

## Funcionalidades Principales

1. **Transcripción de audio:** Convierte comandos de voz en texto utilizando la API de Groq.
2. **Funciones mejoradas:**
    - `obtener_clima`: Describe el clima actual de una ciudad.
    - `calcular_ruta`: Calcula la mejor ruta entre dos ubicaciones.
    - `recomendar_tours`: Proporciona recomendaciones de tours en una ciudad.
3. **Interfaz de usuario:** Basada en Streamlit, permite una interacción fácil y rápida.

## Requisitos Previos

- Python 3.7 o superior.
- Clave de API de Groq. Puedes obtenerla desde [Groq Console](https://console.groq.com).
- Librerías necesarias:
  ```bash
  pip install streamlit sounddevice requests
  ```

## Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Establecer la clave de la API:**
   Inicia la aplicación y proporciona tu clave de API de Groq en la barra lateral.

## Documentación de Groq y Function Calling

### API de Groq
La API de Groq permite procesar texto y audio utilizando modelos avanzados como `llama3-8b-8192`. Puedes consultar más información sobre su uso en la [documentación oficial de Groq](https://console.groq.com/docs).

### Function Calling
Esta funcionalidad permite que el modelo invoque funciones específicas predefinidas en respuesta a las entradas del usuario. Más detalles disponibles en la [guía de Function Calling](https://console.groq.com/docs/tool-use).

## Estructura del Código

### Inicialización de la API Key

La clave de API se ingresa una vez en la barra lateral y se almacena en el estado de sesión:
```python
if "api_key_stored" not in st.session_state:
    st.session_state["api_key_stored"] = ""
```

### Funciones Clave

#### `obtener_clima(ciudad)`
- Envía un comando a la API para obtener información detallada sobre el clima.

#### `calcular_ruta(origen, destino, modo)`
- Calcula la ruta más eficiente entre dos ubicaciones y describe puntos de interés en el camino.

#### `recomendar_tours(ciudad)`
- Genera recomendaciones de tours relevantes y enriquecidas con detalles visuales cuando es posible.

### Transcripción de Audio

Usa la API de Groq para convertir comandos de voz en texto:
```python
url = f"{GROQ_BASE_URL}/audio/transcriptions"
response = requests.post(url, headers=headers, files=files, data=data)
```

### Interfaz de Usuario

Construida con Streamlit, incluye:
- Entrada de la clave API.
- Botón para grabar comandos de voz.
- Respuestas generadas en texto y audio.

## Ejecución

1. Inicia la aplicación:
   ```bash
   streamlit run app.py
   ```

2. Proporciona tu clave API en la barra lateral.
3. Interactúa con las funciones disponibles desde la interfaz.

## Notas

- Asegúrate de que el micrófono esté configurado correctamente para la grabación.
- La clave de API debe tener permisos válidos para usar los servicios de la API de Groq.

## Contribuciones

Si deseas contribuir, envía un pull request o abre un issue en el repositorio.

## Licencia

Este proyecto está bajo la licencia MIT.

