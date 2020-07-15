import { createCard } from './utils';
import http from './http';

document.addEventListener('DOMContentLoaded', () => {
  const cardContainer = document.querySelector('.card-container');
  const searchForm = document.querySelector('#search-form');
  let hasMore = true;
  let next = 20;

  const options = {
    root: null,
    rootMargins: '200px 0px 0px 0px',
    threshold: 0.5,
  };

  const io = new IntersectionObserver(handleIntersection, options);
  io.observe(document.querySelector('footer'));

  searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    hasMore = true;
    next = 0;
    cardContainer.innerHTML = '';
    getFilteredModels(next);
  });

  function handleIntersection(enteries) {
    if (enteries[0].isIntersecting) {
      if (hasMore) {
        setTimeout(() => {
          getFilteredModels(next);
        }, 250);
      }
    }
  }

  async function getFilteredModels(nextSet) {
    const pays = document.getElementById('id_pays').value;
    const ville = document.getElementById('id_ville').value;
    const sexe = document.getElementById('id_sexe').value;
    const cheveux = document.getElementById('id_cheveux').value;
    const yeux = document.getElementById('id_yeux').value;
    const taille = document.getElementById('id_taille').value;
    const searchParams = `pays=${pays}&ville=${ville}&sexe=${sexe}&cheveux=${cheveux}&yeux=${yeux}&taille=${taille}`;

    const { data } = await http.get(
      `models/search?${searchParams}&offset=${nextSet}`
    );
    // If we get no data stop fetching
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
