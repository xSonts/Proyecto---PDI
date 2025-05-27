import os
import io
import base64
import sys
from PIL import Image
sys.path.append(os.path.join(os.getcwd(), 'pytorch-CycleGAN-and-pix2pix'))
from flask import Flask, request, jsonify, render_template
import torch
from torchvision import transforms
from torchvision.transforms import ToPILImage
from models.cycle_gan_model import CycleGANModel
from deepface import DeepFace


emotion_to_style = {
    'happy': 'Puntillismo',
    'sad': 'Ukiyo',
    'angry': 'Ukiyo',
    'fear' : 'Puntillismo',
    'neutral' : 'popart',
    'surprise' : 'popart',
    'disgust':'Ukiyo'


}
 
# Opciones definidas manualmente
class InferenceOptions:
    def __init__(self, checkpoint_path):
        self.gpu_ids = [0] if torch.cuda.is_available() else []
        self.isTrain = False
        self.checkpoints_dir = checkpoint_path
        self.name = 'test'
        self.model = 'cycle_gan'
        self.input_nc = 3
        self.output_nc = 3 
        self.ngf = 64  # Filtros del generador
        self.netG = 'resnet_9blocks'
        self.norm = 'instance'
        self.no_dropout = True
        self.init_type = 'normal'
        self.init_gain = 0.02
        self.direction = 'AtoB'
        self.serial_batches = True
        self.batch_size = 1
        self.load_iter = 0
        self.epoch = 'latest'
        self.preprocess = 'resize_and_crop'
        self.crop_size = 256
        self.load_size = 256
        self.no_flip = True
        self.display_winsize = 256
        self.verbose = False
        self.suffix = ''

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/apply_emotion_style', methods=['POST'])
def apply_style():
    data = request.get_json()
    image_data = data['image']

    image_bytes = base64.b64decode(image_data.split(',')[1])
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    original_size = image.size  # Guardar tamaño original
    
    # Preprocesamiento: mejora visual para webcam
    from PIL import ImageEnhance, ImageFilter
    
    image = image.filter(ImageFilter.SMOOTH_MORE)  # Suavizado
    
    contrast_enhancer = ImageEnhance.Contrast(image)
    image = contrast_enhancer.enhance(1)  # Aumenta contraste
    
    sharpness_enhancer = ImageEnhance.Sharpness(image)
    image = sharpness_enhancer.enhance(1.4)  # Aumenta nitidez
    
    # (Opcional) brillo si las fotos están muy oscuras
    brightness_enhancer = ImageEnhance.Brightness(image)
    image = brightness_enhancer.enhance(0.6)  # Ajusta brillo si es necesario
    
    # Guardar imagen temporal para DeepFace
    temp_path = 'temp.jpg'
    image.save(temp_path)

    # Detectar emoción con DeepFace
    analysis = DeepFace.analyze(img_path=temp_path, actions=['emotion'], enforce_detection=False)
    emotion = analysis[0]['dominant_emotion']
    style = emotion_to_style.get(emotion, 'pop_art')  # por defecto pop_art

    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    image_tensor = transform(image)
    
    checkpoint_path = './checkpoints'  # Define aquí la ruta base de los checkpoints
    opt = InferenceOptions(checkpoint_path)
    opt.name = style
    model = CycleGANModel(opt)
    model.setup(opt)

    data = {'A': image_tensor.unsqueeze(0), 'B': image_tensor.unsqueeze(0), 'A_paths': ['dummy']}
    model.set_input(data)
    model.test()
    output_tensor = model.get_current_visuals()['fake_B']

    output_image = output_tensor.squeeze(0).cpu().detach().clamp(-1, 1)
    output_image = (output_image + 1) / 2
    image_pil = ToPILImage()(output_image)
    image_pil = image_pil.resize(original_size, Image.BICUBIC)

    output_path = os.path.join('static', 'output.png')
    image_pil.save(output_path)

    return jsonify({
        'output_url': '/' + output_path,
        'emotion': emotion,
        'style': style
    })

if __name__ == '__main__':
    app.run(debug=True)
