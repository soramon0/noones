// @ts-ignore
const slider = document.querySelector<HTMLElement>('.drag-slider');

let isDown = false;
let startX;
let scrollLeft;

slider.addEventListener('mousedown', () => {
  isDown = true;
  slider.classList.add('drag-active');
  scrollLeft = slider.scrollLeft;
});

slider.addEventListener('mouseleave', (e: MouseEvent) => {
  isDown = false;
  slider.classList.remove('drag-active');
  // Get where the user clicked and subtrack margin to get correct position
  startX = e.pageX - slider.parentElement.offsetLeft;
});

slider.addEventListener('mouseup', () => {
  isDown = false;
  slider.classList.remove('drag-active');
});

slider.addEventListener('mousemove', (e: MouseEvent) => {
  if (!isDown) return;
  e.preventDefault();
  const x = e.pageX - slider.offsetLeft;
  const offset = (x - startX) * 3;
  slider.scrollLeft = scrollLeft - offset;
});
