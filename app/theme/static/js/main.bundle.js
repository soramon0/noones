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