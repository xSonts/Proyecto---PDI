const video = document.getElementById('video');
const captureButton = document.getElementById('capture');
const styleInfo = document.getElementById('style-info');

// Solicitar acceso a la cámara
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    alert('Error al acceder a la cámara: ' + err);
  });

captureButton.addEventListener('click', () => {
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const imageBase64 = canvas.toDataURL('image/jpeg');

  // Mostrar el spinner
  document.getElementById('loader').style.display = 'flex';
  const originalImg = document.getElementById('original-image');
originalImg.src = imageBase64;
originalImg.style.display = 'block';

  fetch('/api/apply_emotion_style', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: imageBase64 })
  })
    .then(res => res.json())
    .then(data => {
  // Ocultar el spinner
  document.getElementById('loader').style.display = 'none';

  // Mostrar la imagen con estilo aplicado
  const img = document.getElementById('styled-image');
  img.src = data.output_url + '?t=' + new Date().getTime();
document.getElementById('resultado-imagenes').style.display = 'flex';

  // Mostrar descripción del estilo
  const info = getStyleDescription(data.style);
  styleInfo.innerHTML = `<strong>Emoción detectada:</strong> ${data.emotion}<br>
                         <strong>Estilo aplicado:</strong> ${data.style}<br><br>${info}`;
  styleInfo.style.display = 'block';

  // Mostrar solo el grupo de imágenes correspondiente al estilo
  mostrarImagenesPorEstilo(data.style);
})
});

function getStyleDescription(style) {
  switch (style.toLowerCase()) {
    case 'puntillismo':
      return 'El puntillismo es una técnica pictórica que consiste en la aplicación de pequeños puntos de colores puros sobre el lienzo. Estos puntos, al observarse a distancia, se fusionan ópticamente para crear imágenes completas con una vibrante riqueza tonal. Este estilo enfatiza la separación de colores y la percepción visual, buscando representar la luz y la forma a través del contraste de puntos.';
    case 'ukiyo':
      return 'Ukiyo-e es un género de arte japonés que floreció entre los siglos XVII y XIX, conocido por sus grabados en madera y pinturas que representan escenas de la vida cotidiana, paisajes y retratos. Se distingue por sus líneas claras, colores planos y composiciones equilibradas, que transmiten tanto la belleza efímera como aspectos culturales y sociales del Japón de la época. Uno de sus principales representantes es Katsushika Hokusai.';
    case 'popart':
      return 'El Pop Art surge como un movimiento artístico que integra imágenes y temáticas de la cultura popular y los medios de comunicación de masas. Se caracteriza por el uso de colores vivos, contrastes fuertes y composiciones llamativas, con la intención de cuestionar y reflejar la sociedad de consumo y la producción en masa. Este estilo resalta elementos cotidianos, otorgándoles un nuevo valor visual y cultural. Uno de sus principales respresentantes es Roy Lichtenstein';
  }
}

function mostrarImagenesPorEstilo(style) {
  const estilos = ['puntillismo', 'ukiyo', 'popart'];

  estilos.forEach(estilo => {
    const div = document.getElementById(`style-${estilo}`);
    if (div) div.style.display = (estilo === style.toLowerCase()) ? 'block' : 'none';
  });
}


function procesarFoto() {
  document.getElementById("loader").style.display = "block";

  // Simula procesamiento (usa aquí tu llamada a IA)
  fetch("/procesar-foto", { method: "POST" }) 
    .then(res => res.json())
    .then(data => {
      document.getElementById("loader").style.display = "none";
      // Mostrar la imagen procesada
      document.getElementById("imagenProcesada").src = data.url;
    });
    
}
// Lógica del modal fuera de otras funciones
const modal = document.getElementById("infoModal");
const btn = document.getElementById("infoBtn");
const close = document.querySelector(".close");

btn.onclick = function () {
  modal.classList.remove("hidden");
};

close.onclick = function () {
  modal.classList.add("hidden");
};

window.onclick = function (event) {
  if (event.target === modal) {
    modal.classList.add("hidden");
  }
};