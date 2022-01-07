const backdrop = document.getElementById('lightbox-backdrop');
const lightbox = document.getElementById('lightbox');
const closeButton = lightbox.querySelector('#lightbox-close');
const prevButton = lightbox.querySelector('#lightbox-prev');
const nextButton = lightbox.querySelector('#lightbox-next');
const lightboxImg = lightbox.querySelector('#lightbox-img');
const galleryContainer = document.getElementById('gallery-container');
const gallery = Array.from(galleryContainer.children);

let currentIndex = 0;

function toggleLightbox() {
  if (lightbox.classList.contains('scale-0')) {
    backdrop.classList.remove('hidden');
    lightbox.classList.remove('scale-0');
    lightbox.classList.remove('opacity-0');
  } else {
    lightbox.classList.add('opacity-0');
    lightbox.classList.add('scale-0');
    backdrop.classList.add('hidden');
  }
}

function setImgByIndex(index) {
  currentIndex = index;
  const el = gallery[currentIndex].firstElementChild;
  // @ts-ignore
  lightboxImg.src = el.src;
}

function showElement(element) {
  if (element.classList.contains('hidden')) {
    element.classList.remove('hidden');
  }
}

gallery.forEach((entry) => {
  entry.addEventListener('click', () => {
    const img = entry.firstElementChild;
    // continue if entry has a child
    // Html structure should be a div that has an image inside it
    if (img) {
      // get the index of which image the user clicked on
      // @ts-ignore
      currentIndex = parseInt(entry.dataset.id, 10);

      // Hide prev button if the user clicks on the first image
      if (currentIndex <= 0) {
        prevButton.classList.add('hidden');
      } else {
        showElement(prevButton);
      }

      // Hide next button if the user clicks on the last image
      if (currentIndex >= gallery.length - 1) {
        nextButton.classList.add('hidden');
      } else {
        showElement(nextButton);
      }

      // @ts-ignore
      const src = img.src;

      if (src) {
        // @ts-ignore
        lightboxImg.src = src;
        toggleLightbox();
      }
    }
  });
});

prevButton.addEventListener('click', () => {
  const index = currentIndex - 1;

  if (index >= 0) {
    setImgByIndex(index);

    showElement(nextButton);
  }

  if (index <= 0) prevButton.classList.add('hidden');
});

nextButton.addEventListener('click', () => {
  const index = currentIndex + 1;
  const galleryLength = gallery.length - 1;

  if (index <= galleryLength) {
    setImgByIndex(index);

    showElement(prevButton);
  }

  if (index >= galleryLength) nextButton.classList.add('hidden');
});

backdrop.addEventListener('click', toggleLightbox);
closeButton.addEventListener('click', toggleLightbox);
