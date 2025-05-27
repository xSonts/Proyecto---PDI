import torch
from PIL import Image
from torchvision import transforms
from models import networks
from options.test_options import TestOptions
from models.cycle_gan_model import CycleGANModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model(checkpoint_path):
    opt = TestOptions().parse()
    opt.checkpoints_dir = './checkpoints'
    opt.name = 'estilo'  # cambia por el estilo si usas varios
    opt.model = 'cycle_gan'
    opt.no_dropout = True
    opt.num_threads = 0
    opt.batch_size = 1
    opt.load_size = 256
    opt.crop_size = 256
    opt.gpu_ids = [0] if torch.cuda.is_available() else []
    opt.num_test = 1
    opt.load_epoch = 'latest'
    opt.phase = 'test'
    opt.isTrain = False
    opt.preprocess = 'resize_and_crop'
    opt.input_nc = 3
    opt.output_nc = 3
    opt.netG = 'resnet_9blocks'
    opt.norm = 'instance'
    opt.init_type = 'normal'
    opt.init_gain = 0.02
    opt.serial_batches = True

    model = CycleGANModel(opt)
    model.setup(opt)
    model.eval()

    # Cargar pesos manualmente
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.netG_A.load_state_dict(checkpoint['model']['netG_A'])
    model.netG_B.load_state_dict(checkpoint['model']['netG_B'])
    return model

def transform_image(image_path):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(256),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5),
                             (0.5, 0.5, 0.5)),
    ])
    img = Image.open(image_path).convert('RGB')
    return transform(img).unsqueeze(0)

def inference(model, input_image_tensor):
    with torch.no_grad():
        model.set_input({'A': input_image_tensor, 'A_paths': ['dummy']})
        model.test()
        visuals = model.get_current_visuals()
        fake_img = visuals['fake_B'].cpu()
        fake_img = (fake_img + 1) / 2
        fake_img = torch.clamp(fake_img, 0, 1)
        fake_img = transforms.ToPILImage()(fake_img.squeeze())
        return fake_img
