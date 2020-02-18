const slider = document.querySelector('.drag-slider');

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
