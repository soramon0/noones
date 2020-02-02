const track = document.querySelector('.carousel-track')
const slides = Array.from(track.children)
const prevButton = document.querySelector('.carousel-left')
const nextButton = document.querySelector('.carousel-right')

const slideWidth = slides[0].getBoundingClientRect().width

// If we have only one photo in the slide
// Hide the buttons
if (slides.length <= 1) {
  prevButton.style.display = 'none'
  nextButton.style.display = 'none'
}

// Arrange the slides next to one another
const setSlidePosition = (slide, index) => {
  // Add the current-slide class manually due to html library limitions
  if (index === 0) {
    slide.classList.add('current-slide')
  }

  slide.style.left = (slideWidth * index) + 'px'
}

slides.forEach(setSlidePosition)

const moveToSlide = (targetSlide, currentSlide) => {
  const amountToMove = targetSlide.style.left

  track.style.transform = `translateX(-${amountToMove})`
  currentSlide.classList.remove('current-slide')
  targetSlide.classList.add('current-slide')
}

// When I click left, move slides to the left
prevButton.addEventListener('click', () => {
  const currentSlide = track.querySelector('.current-slide')
  const prevSlide = currentSlide.previousElementSibling
  const index = slides.indexOf(prevSlide)

  // Hide the prev button if we're at the first slide
  // But only if moved once
  if (index == 0) {
    prevButton.style.display = 'none'
  }

  if (!prevSlide) {
    return
  }

  // if we can go back; show the next button
  if (prevSlide) {
    nextButton.style.display = 'block'
  }

  moveToSlide(prevSlide, currentSlide)
})

// When I click right, move slides to the right
nextButton.addEventListener('click', () => {
  const currentSlide = track.querySelector('.current-slide')
  const nextSlide = currentSlide.nextElementSibling

  // Hide the next button if we're at the last slide
  const index = slides.indexOf(currentSlide) + 1
  if (index == slides.length - 1) {
    nextButton.style.display = 'none'
  }

  if (nextSlide) {
    prevButton.style.display = 'block'
  }

  moveToSlide(nextSlide, currentSlide)
})