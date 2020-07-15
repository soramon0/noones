import { lazyLoad, createCard } from './utils';
import http from './http';

document.addEventListener('DOMContentLoaded', () => {
  // TODO(karim): Add animations
  const cardContainer = document.querySelector('.card-container');
  let hasMore = true;
  let next = 20;

  const options = {
    root: null,
    rootMargins: '200px 0px 0px 0px',
    threshold: 0.5,
  };

  const io = new IntersectionObserver(handleIntersection, options);
  io.observe(document.querySelector('footer'));

  // Lazy load initial imgs
  const cards = Array.from(cardContainer.children);
  cards.forEach((card) => {
    lazyLoad(card.children[0].children[0], {
      rootMargins: '300px 0px 0px 0px',
    });
  });

  function handleIntersection(enteries) {
    if (enteries[0].isIntersecting) {
      if (hasMore) {
        setTimeout(() => {
          getModels(next);
        }, 250);
      }
    }
  }

  async function getModels(nextSet) {
    const { data } = await http.get(`models/?offset=${nextSet}`);

    if (data.next) {
      const url = new URL(data.next);
      const offset = url.searchParams.get('offset');
      next = offset;
    } else {
      hasMore = false;
    }

    data.results.forEach((model) => createCard(model, cardContainer));
  }
});
