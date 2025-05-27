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