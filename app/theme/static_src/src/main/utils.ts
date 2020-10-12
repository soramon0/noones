import http from './http'

export function lazyLoad(targets, op: IntersectionObserverInit = {}) {
	const options = {
		root: op.root || null,
		rootMargin: op.rootMargin || '0px',
		threshold: op.threshold || 0,
	};

	function handle(enteries: IntersectionObserverEntry[]) {
		enteries.forEach((entry) => {
			if (entry.isIntersecting) {
				const img = entry.target as HTMLImageElement;

				if (img.src) return;

				img.src = img.getAttribute('data-src');
				io.unobserve(img);
			}
		});
	}

	const io = new IntersectionObserver(handle, options);
	io.observe(targets);
}

export function createCard(data, parent) {
	// Create Card
	const card = document.createElement('div');
	const cardHead = document.createElement('div');
	const img = document.createElement('img');
	const skewLine = document.createElement('div');
	const nameTag = document.createElement('div');
	const cardBody = document.createElement('div');
	const leftText = document.createElement('div');
	const countryText = document.createElement('p');
	const cityText = document.createElement('p');
	const profileButton = document.createElement('a');

	nameTag.title = `${data.profile.first_name} ${data.profile.last_name}`;

	// Style Card
	card.className =
		'w-72 mb-4 overflow-hidden rounded-lg shadow relative sm:w-64 sm:mr-4';
	cardHead.className = 'h-56 bg-gray-100';
	img.className = 'w-full h-full object-fit';
	skewLine.className = '-mt-4 w-full h-10 transform -skew-y-6 bg-white';
	nameTag.className =
		'-mt-16 mr-4 py-2 px-4 truncate w-48 uppercase tracking-wider bg-white rounded text-center shadow absolute right-0';
	cardBody.className =
		'mt-6 px-4 pb-4 text-sm flex justify-between items-center relative';
	leftText.className = 'tracking-wide';
	countryText.className = 'uppercase tracking-wider';
	cityText.className = 'capitalize text-gray-800 font-semibold';
	profileButton.className =
		'px-4 py-3 text-xs rounded-lg bg-black hover:bg-gray-700 text-white uppercase tracking-wide';

	// Add Content
	const name = `${data.profile.first_name} ${data.profile.last_name}`;
	// Check For Img
	if (data.image) {
		img.src = data.image;
	} else {
		img.src = '/static/images/noc-models-mission.jpg';
	}

	img.alt = name;
	nameTag.textContent = name;

	countryText.textContent = data.profile.country;
	cityText.textContent = data.profile.city;

	profileButton.textContent = 'Visit Profile';
	profileButton.href = `/models/${data.profile.id}`;

	// Create Structure
	card.appendChild(cardHead);
	cardHead.appendChild(img);
	cardHead.appendChild(skewLine);
	cardHead.appendChild(nameTag);
	card.appendChild(cardBody);
	cardBody.appendChild(leftText);
	leftText.appendChild(countryText);
	leftText.appendChild(cityText);
	cardBody.appendChild(profileButton);

	parent.appendChild(card);
}

export async function isOnline(cb) {
	const connectionContainer = document.getElementById('checkConnection');
	const reconnectButton = document.getElementById('checkConnection-reconnect');
	const connectionText = document.getElementById('checkConnection-text');
	const indicator = document.getElementById('checkConnection-indicator');

	const handleOnlineUI = async () => {
		reconnectButton.textContent = 'Reconnecting...';

		if (navigator.onLine) {
			// disbaled button and send request
			reconnectButton.setAttribute('disabled', 'true');
			await cb();

			// update ui
			indicator.classList.add('bg-green-500');
			connectionText.textContent = 'Connection restored.';
			reconnectButton.textContent = 'Connected.';

			// remove ui and click event
			setTimeout(() => {
				connectionContainer.classList.add('-translate-y-full');
				reconnectButton.removeEventListener('click', handleOnlineUI);
			}, 1500);
		} else {
			connectionText.textContent = 'Connection lost.';
			indicator.classList.remove('bg-green-500');
			indicator.classList.add('bg-red-400');

			// TODO(karim): add a spinner
			setTimeout(() => {
				// give enought time for the reconnect text to show
				reconnectButton.textContent = 'No internet. try again';
			}, 400);
		}
	};

	if (navigator.onLine) {
		// if we have internet; send the fetch request
		await cb();
	} else {
		// Reset UI
		reconnectButton.textContent = 'Reconnect';
		connectionContainer.classList.remove('-translate-y-full');
		indicator.classList.remove('bg-green-500');
		indicator.classList.add('bg-red-400');
		connectionText.textContent = 'Connection lost.';
		reconnectButton.removeAttribute('disabled');

		reconnectButton.addEventListener('click', handleOnlineUI);
	}
}

const appearOptions: IntersectionObserverInit = {
	threshold: 0,
	rootMargin: '0px 0px -250px 0px',
};

function handleIntersection(entries: IntersectionObserverEntry[]) {
	entries.forEach((entry) => {
		if (!entry.isIntersecting) return;

		entry.target.classList.add('appear');
		appearOnScroll.unobserve(entry.target);
	});
}

export const appearOnScroll = new IntersectionObserver(
	handleIntersection,
	appearOptions
);

export function handleCountryChange() {
	const countryField = document.querySelector<HTMLSelectElement>('#id_country')
	const cityField = document.querySelector('#id_city')

	const initialOption = document.createElement('option');
	initialOption.text = "Select a City";
	initialOption.disabled = true;
	initialOption.selected = true;
	cityField.appendChild(initialOption);	
	
	if (countryField && cityField) {
		countryField.addEventListener('change', async (e) => {
			const { value, options, selectedIndex } = e.target as HTMLSelectElement;
			const countryName = options[selectedIndex].text;

			setCities(value, countryName, cityField);
		})
	}
}

export async function setCities(countryCode:string, countryName:string, cityField: Element){
	try {
		const { data } = await http.get('city/', {
			params: {
				code: countryCode,
				country: countryName
			}
		});

		cityField.innerHTML = '';

		data.forEach(city => {
			const option = document.createElement('option');
			option.value = option.text = city.name;
			cityField.appendChild(option);
		});
	} catch {}
}