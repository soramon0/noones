const hamburger = document.getElementById('hamburger');
const sidenav = document.getElementById('sidedrawer');
const sidenavClose = document.getElementById('sidedrawer-close');

hamburger.addEventListener('click', () => {
  sidenav.classList.add('open');
});

sidenavClose.addEventListener('click', function () {
  sidenav.classList.remove('open');
});
