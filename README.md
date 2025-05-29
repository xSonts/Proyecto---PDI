# 🎭 Emotion-Based Art Style Transfer

Este proyecto permite al usuario tomarse una foto con la cámara web, detectar su emoción mediante DeepFace y aplicar automáticamente un estilo artístico correspondiente usando modelos entrenados con CycleGAN.

## 💡 ¿Cómo funciona?

1. El usuario accede a la app web y se toma una foto.
2. La foto es enviada al backend Flask.
3. Se detecta la emoción facial con DeepFace.
4. Se selecciona un modelo de estilo artístico (CycleGAN) en función de la emoción detectada.
5. Se genera una imagen estilizada y se muestra al usuario.

## 🎨 Mapeo de emociones a estilos

| Emoción detectada | Estilo artístico aplicado |
|-------------------|---------------------------|
| happy             | Puntillismo               |
| sad               | Ukiyo-e                   |
| neutral           | Pop Art                   |

## 📁 Estructura del proyecto

emotion-art-style-transfer/
│
├── app.py # Backend principal en Flask
├── templates/ # HTML con Jinja2
│ └── index.html
│ └── result.html
├── static/ # Archivos estáticos (CSS, JS, etc.)
├── models/ # Checkpoints de modelos CycleGAN
│ ├── puntillismo/
│ ├── ukiyo/
│ └── popart/
├── utils/ # Funciones de inferencia y preprocesamiento
│ ├── preprocess.py
│ └── style_transfer.py
├── uploads/ # Carpeta temporal para imágenes de usuario
├── output/ # Carpeta para resultados estilizados
├── requirements.txt # Librerías necesarias
├── .gitignore # Archivos ignorados por git
└── README.md # Este archivo

## 🚀 Cómo ejecutar

1. Clona el repositorio:
   ```bash
   git clone https://github.com/xSonts/Proyecto---PDI.git
2. Clona el repositorio de CycleGan
   ```bash
   git clone https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.git
   
Instala las dependencias:
bash
Copiar
Editar
pip install -r requirements.txt
Ejecuta la aplicación:

bash
Copiar
Editar
python app.py
