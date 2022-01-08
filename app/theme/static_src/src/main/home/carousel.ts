const track = document.querySelector<HTMLElement>('.carousel-track');
const carouselLeft = document.querySelector<HTMLElement>('.carousel-left');
const carouselNext = document.querySelector<HTMLElement>('.carousel-right');
const slides = Array.from(track.children);
const slideWidth = slides[0].getBoundingClientRect().width;

// If we have only one photo in the slide
// Hide the buttons
if (slides.length <= 1) {
	carouselLeft.style.display = 'none';
	carouselNext.style.display = 'none';
}

// Arrange the slides next to one another
const setSlidePosition = (slide, index) => {
	// Add the current-slide class manually due to html library limitions
	if (index === 0) {
		slide.classList.add('current-slide');
	}

	slide.style.left = slideWidth * index + 'px';
};

slides.forEach(setSlidePosition);

const moveToSlide = (targetSlide, currentSlide) => {
	const amountToMove = targetSlide.style.left;

	track.style.transform = `translateX(-${amountToMove})`;
	currentSlide.classList.remove('current-slide');
	targetSlide.classList.add('current-slide');
};
// When I click left, move slides to the left
carouselLeft.addEventListener('click', () => {
	const currentSlide = track.querySelector('.current-slide');
	const prevSlide = currentSlide.previousElementSibling;
	const index = slides.indexOf(prevSlide);

	// Hide the prev button if we're at the first slide
	// But only if moved once
	if (index == 0) {
		carouselLeft.style.display = 'none';
	}

	if (!prevSlide) {
		return;
	}

	// if we can go back; show the next button
	if (prevSlide) {
		carouselNext.style.display = 'block';
	}

	moveToSlide(prevSlide, currentSlide);
});

// When I click right, move slides to the right
carouselNext.addEventListener('click', () => {
	const currentSlide = track.querySelector('.current-slide');
	const nextSlide = currentSlide.nextElementSibling;

	// Hide the next button if we're at the last slide
	const index = slides.indexOf(currentSlide) + 1;
	if (index == slides.length - 1) {
		carouselNext.style.display = 'none';
	}

	if (nextSlide) {
		carouselLeft.style.display = 'block';
	}

	moveToSlide(nextSlide, currentSlide);
});
