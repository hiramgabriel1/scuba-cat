# Scooba - Detector de Gatos

Aplicación de detección de gestos en tiempo real que reproduce un video y música cuando detecta un gesto específico con la mano.

## Funcionalidad

- Usa la cámara web para detectar gestos de manos en tiempo real
- Detecta el gesto "Scooba": pulgar e índice rapproados (distancia < 0.1) + al menos 3 dedos extendido
- Cuando se detecta el gesto, reproduce un video y una canción en bucle
- El video se muestra en la esquina superior izquierda

## Requisitos

- Python 3.9+
- Cámara web
- Archivo `hand_landmarker.task` (modelo de MediaPipe)
- Archivo `scooba_video.mp4` (video a reproducir)
- Archivo `scuba_song.mp3` (música a reproducir)

## Instalación

1. Crear entorno virtual:
```bash
python3 -m venv venv
```

2. Activar entorno virtual:
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Descargar el modelo de MediaPipe:
   Descarga `hand_landmarker.task` desde [MediaPipe Models](https://developers.google.com/mediapipe/solutions/models/hand_landmarker)

## Cómo ejecutarlo

```bash
python main.py
```

El programa abrirá una ventana mostrando la cámara web. Cuando hagas el gesto con la mano, reproducirá el video y la música.

## Gesto Scooba

El gesto detectado es:
- Pulgar e índice muy rapproados
- Al menos 3 dedos (medio, anular, meñique) extendidos
- Similar a hacer "corn" con los dedos para simular orejas de gato