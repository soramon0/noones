const registerForm = document.querySelector<HTMLFormElement>('.register-form');
const registerBtn = registerForm.querySelector('.register-btn');
const sections = Array.from(registerForm.children).slice(1);

registerForm.addEventListener('submit', (e) => {
	e.preventDefault();
});

registerBtn.addEventListener('click', () => {
	registerForm.submit();
});

function HandleSectionMovment(current, target) {
	current.classList.remove('current');
	current.classList.add('opacity-0');
	current.classList.add('invisible');
	current.classList.add('absolute');

	target.classList.remove('opacity-0');
	target.classList.remove('invisible');
	target.classList.remove('absolute');
	target.classList.add('current');
}

// This depends on the structure of the html
sections.forEach((section) => {
	// Find all the buttons
	const btns = Array.from(section.querySelector('.button-container').children);

	// Loop through through them and add a click
	// listener depending on the button class type
	btns.forEach((btn) => {
		if (btn.classList.contains('next')) {
			btn.addEventListener('click', () => {
				// Find the section with the current class
				// to hide it and show the next section
				const currentSection = registerForm.querySelector('.current');
				const nextSection = currentSection.nextElementSibling;
				HandleSectionMovment(currentSection, nextSection);

				if (nextSection.classList.contains('translate-x-full')) {
					currentSection.classList.add('-translate-x-full');
					nextSection.classList.remove('translate-x-full');
				}
			});
		}

		if (btn.classList.contains('previous')) {
			btn.addEventListener('click', () => {
				// Find the section with the current class
				// to hide it and show the previous section
				const currentSection = registerForm.querySelector('.current');
				const prevSection = currentSection.previousElementSibling;
				HandleSectionMovment(currentSection, prevSection);

				if (prevSection.classList.contains('-translate-x-full')) {
					currentSection.classList.add('translate-x-full');
					prevSection.classList.remove('-translate-x-full');
				}
			});
		}
	});
});
