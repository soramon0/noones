// @ts-ignore
const glider = new Glider(document.querySelector('.glider'), {
	slidesToShow: 2,
	slidesToScroll: 2,
	draggable: true,
	dots: '.dots',
	arrows: {
		prev: '.glider-prev',
		next: '.glider-next',
	},
	responsive: [
		{
			// screens greater than >= 640px
			breakpoint: 640,
			settings: {
				slidesToShow: 3,
				slidesToScroll: 3,
			},
		},
		{
			// screens greater than >= 1024px
			breakpoint: 1024,
			settings: {
				slidesToShow: 4,
				slidesToScroll: 4,
			},
		},
	],
});
