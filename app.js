// Importer les modules nécessaires
import Swiper from 'swiper';

export function chooseRandomImage() {

  // Lire les dossiers dans img 
  fs.readdir('data/images', (err, folders) => {

    // Choisir un dossier aléatoire
    const randomFolder = folders[Math.floor(Math.random() * folders.length)];

    console.log(randomFolder)

    // Lire les images dans ce dossier
    fs.readdir(`data/images/${randomFolder}`, (err, files) => {
      
      // Filtrer pour ne garder que les images
      const images = files.filter(file => file.endsWith('.png'));

      // Choisir une image aléatoire
      const randomImage = `data/images/${randomFolder}/${images[Math.floor(Math.random() * images.length)]}`;
      
      // Afficher l'image 
      // document.getElementById('photo').src = randomImage;
      return randomImage;

    });
  });
}

export function initApp() {

  const img = chooseRandomImage();
  
  document.getElementById('photo').src = img;

}

export function initSwiper() {

  new Swiper('.swiper');

}

initApp(); 
initSwiper();