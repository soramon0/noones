/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/main/index.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./node_modules/js-cookie/src/js.cookie.js":
/*!*************************************************!*\
  !*** ./node_modules/js-cookie/src/js.cookie.js ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_RESULT__;/*!
 * JavaScript Cookie v2.2.1
 * https://github.com/js-cookie/js-cookie
 *
 * Copyright 2006, 2015 Klaus Hartl & Fagner Brack
 * Released under the MIT license
 */
;(function (factory) {
	var registeredInModuleLoader;
	if (true) {
		!(__WEBPACK_AMD_DEFINE_FACTORY__ = (factory),
				__WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ?
				(__WEBPACK_AMD_DEFINE_FACTORY__.call(exports, __webpack_require__, exports, module)) :
				__WEBPACK_AMD_DEFINE_FACTORY__),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
		registeredInModuleLoader = true;
	}
	if (true) {
		module.exports = factory();
		registeredInModuleLoader = true;
	}
	if (!registeredInModuleLoader) {
		var OldCookies = window.Cookies;
		var api = window.Cookies = factory();
		api.noConflict = function () {
			window.Cookies = OldCookies;
			return api;
		};
	}
}(function () {
	function extend () {
		var i = 0;
		var result = {};
		for (; i < arguments.length; i++) {
			var attributes = arguments[ i ];
			for (var key in attributes) {
				result[key] = attributes[key];
			}
		}
		return result;
	}

	function decode (s) {
		return s.replace(/(%[0-9A-Z]{2})+/g, decodeURIComponent);
	}

	function init (converter) {
		function api() {}

		function set (key, value, attributes) {
			if (typeof document === 'undefined') {
				return;
			}

			attributes = extend({
				path: '/'
			}, api.defaults, attributes);

			if (typeof attributes.expires === 'number') {
				attributes.expires = new Date(new Date() * 1 + attributes.expires * 864e+5);
			}

			// We're using "expires" because "max-age" is not supported by IE
			attributes.expires = attributes.expires ? attributes.expires.toUTCString() : '';

			try {
				var result = JSON.stringify(value);
				if (/^[\{\[]/.test(result)) {
					value = result;
				}
			} catch (e) {}

			value = converter.write ?
				converter.write(value, key) :
				encodeURIComponent(String(value))
					.replace(/%(23|24|26|2B|3A|3C|3E|3D|2F|3F|40|5B|5D|5E|60|7B|7D|7C)/g, decodeURIComponent);

			key = encodeURIComponent(String(key))
				.replace(/%(23|24|26|2B|5E|60|7C)/g, decodeURIComponent)
				.replace(/[\(\)]/g, escape);

			var stringifiedAttributes = '';
			for (var attributeName in attributes) {
				if (!attributes[attributeName]) {
					continue;
				}
				stringifiedAttributes += '; ' + attributeName;
				if (attributes[attributeName] === true) {
					continue;
				}

				// Considers RFC 6265 section 5.2:
				// ...
				// 3.  If the remaining unparsed-attributes contains a %x3B (";")
				//     character:
				// Consume the characters of the unparsed-attributes up to,
				// not including, the first %x3B (";") character.
				// ...
				stringifiedAttributes += '=' + attributes[attributeName].split(';')[0];
			}

			return (document.cookie = key + '=' + value + stringifiedAttributes);
		}

		function get (key, json) {
			if (typeof document === 'undefined') {
				return;
			}

			var jar = {};
			// To prevent the for loop in the first place assign an empty array
			// in case there are no cookies at all.
			var cookies = document.cookie ? document.cookie.split('; ') : [];
			var i = 0;

			for (; i < cookies.length; i++) {
				var parts = cookies[i].split('=');
				var cookie = parts.slice(1).join('=');

				if (!json && cookie.charAt(0) === '"') {
					cookie = cookie.slice(1, -1);
				}

				try {
					var name = decode(parts[0]);
					cookie = (converter.read || converter)(cookie, name) ||
						decode(cookie);

					if (json) {
						try {
							cookie = JSON.parse(cookie);
						} catch (e) {}
					}

					jar[name] = cookie;

					if (key === name) {
						break;
					}
				} catch (e) {}
			}

			return key ? jar[key] : jar;
		}

		api.set = set;
		api.get = function (key) {
			return get(key, false /* read as raw */);
		};
		api.getJSON = function (key) {
			return get(key, true /* read as json */);
		};
		api.remove = function (key, attributes) {
			set(key, '', extend(attributes, {
				expires: -1
			}));
		};

		api.defaults = {};

		api.withConverter = init;

		return api;
	}

	return init(function () {});
}));


/***/ }),

/***/ "./src/main/carousel.js":
/*!******************************!*\
  !*** ./src/main/carousel.js ***!
  \******************************/
/*! no static exports found */
/***/ (function(module, exports) {

const track = document.querySelector('.carousel-track')
const prevButton = document.querySelector('.carousel-left')
const nextButton = document.querySelector('.carousel-right')

// If this file loads on other pages
// Track will be undefiend
if (!track) {
  return
}

const slides = Array.from(track.children)
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

/***/ }),

/***/ "./src/main/drag.js":
/*!**************************!*\
  !*** ./src/main/drag.js ***!
  \**************************/
/*! no static exports found */
/***/ (function(module, exports) {

const slider = document.querySelector('.drag-slider');

if (!slider) return;

let isDown = false;
let startX;
let scrollLeft;

slider.addEventListener('mousedown', (e) => {
  isDown = true;
  slider.classList.add('drag-active')
  scrollLeft = slider.scrollLeft
});

slider.addEventListener('mouseleave', (e) => {
  isDown = false;
  slider.classList.remove('drag-active')
  // Get where the user clicked and subtrack margin to get correct position
  startX = e.pageX - slider.parentElement.offsetLeft
});

slider.addEventListener('mouseup', (e) => {
  isDown = false;
  slider.classList.remove('drag-active')
});

slider.addEventListener('mousemove', (e) => {
  if (!isDown) return;
  e.preventDefault()
  const x = e.pageX - slider.offsetLeft
  const offset = (x - startX) * 3
  slider.scrollLeft = scrollLeft - offset;
});

/***/ }),

/***/ "./src/main/index.js":
/*!***************************!*\
  !*** ./src/main/index.js ***!
  \***************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _navbar__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./navbar */ "./src/main/navbar.js");
/* harmony import */ var _navbar__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_navbar__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _carousel__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./carousel */ "./src/main/carousel.js");
/* harmony import */ var _carousel__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_carousel__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _drag__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./drag */ "./src/main/drag.js");
/* harmony import */ var _drag__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_drag__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _model_modal__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./model-modal */ "./src/main/model-modal.js");





/***/ }),

/***/ "./src/main/model-modal.js":
/*!*********************************!*\
  !*** ./src/main/model-modal.js ***!
  \*********************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var js_cookie__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! js-cookie */ "./node_modules/js-cookie/src/js.cookie.js");
/* harmony import */ var js_cookie__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(js_cookie__WEBPACK_IMPORTED_MODULE_0__);


const contactButton = document.getElementById('model-contact')
const backdrop = document.getElementById('model-backdrop')
const modal = document.getElementById('model-modal')
const contactForm = document.getElementById('model-form')
const sendContactButton = document.getElementById('send-contact')
const modalFlash = document.getElementById('modal-flash')
const modalMessage = document.getElementById('modal-message')

function toggleModal() {
    if (modal.classList.contains('hidden')) {
        backdrop.classList.remove('hidden')
        modal.classList.remove('hidden')
    } else {
        backdrop.classList.add('hidden')
        modal.classList.add('hidden')
    }
}

function handleErrorRes(errors) {    
    // const div = document.createElement('div')
    // errors.email.forEach(e => {
    //     div.textContent = e
    //     id_email.insertBefore(div, id_email)
    // });
    console.log(errors)
}

function disableSendingButton(sending) {
    if (sending) {
        sendContactButton.disabled = sending
        sendContactButton.textContent = 'sending'
    } else {
        sendContactButton.disabled = sending
        sendContactButton.textContent = 'send'
    }
}

function sendContactRequest(e) {
    // Disable button until request is done
    disableSendingButton(true)

    e.preventDefault()
    const data = {
        'model_id': document.getElementById('id_model_id').value,
        'model_nom': document.getElementById('id_model_nom').value,
        'email': document.getElementById('id_email').value,
        'phone': document.getElementById('id_phone').value,
    }


    fetch('/models/request', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'X-CSRFToken': js_cookie__WEBPACK_IMPORTED_MODULE_0___default.a.get('csrftoken'),
            mode: 'same-origin',
        }
    })
    .then(blob => blob.json())
    .then((res) => {
        disableSendingButton(false)
        if (res.hasOwnProperty('errors')) {
            handleErrorRes(res.errors)
            return
        }
        // Request was successfull
        modalMessage.textContent = res.message
        modalFlash.classList.remove('hidden')
        modalFlash.classList.add('opacity-100')
        setTimeout(() => {
            modalFlash.classList.remove('opacity-100')
            modalFlash.classList.add('hidden')
        }, 3000)
    })
    .catch((e) => {
        disableSendingButton(false)
        console.log(e)
    })
}

contactButton.addEventListener('click', toggleModal)
backdrop.addEventListener('click', toggleModal)
contactForm.addEventListener('submit', sendContactRequest)


/***/ }),

/***/ "./src/main/navbar.js":
/*!****************************!*\
  !*** ./src/main/navbar.js ***!
  \****************************/
/*! no static exports found */
/***/ (function(module, exports) {

const hamburger = document.getElementById("hamburger");
const sidenav = document.getElementById("sidedrawer");
const sidenavClose = document.getElementById("sidedrawer-close");

hamburger.addEventListener("click", function() {
  sidenav.classList.add("open");
});

sidenavClose.addEventListener("click", function() {
  sidenav.classList.remove("open");
});


/***/ })

/******/ });
//# sourceMappingURL=main.bundle.js.map