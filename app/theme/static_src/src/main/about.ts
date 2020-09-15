import { appearOnScroll, lazyLoad } from './utils';

document.addEventListener('DOMContentLoaded', () => {
	const faders = document.querySelectorAll('.fade');
	const slides = document.querySelectorAll('.slide-in');
	const images = document.querySelectorAll('.slide-in img');
	const ImgOptions: IntersectionObserverInit = {
		rootMargin: '500px 0px 0px 0px',
		threshold: 0,
	};

	images.forEach((img) => {
		lazyLoad(img, ImgOptions);
	});

	faders.forEach((fader) => {
		appearOnScroll.observe(fader);
	});

	slides.forEach((slide) => {
		appearOnScroll.observe(slide);
	});
});
