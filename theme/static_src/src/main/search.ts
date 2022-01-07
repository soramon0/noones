import { createCard } from './utils';
import http from './http';

document.addEventListener('DOMContentLoaded', () => {
  const cardContainer = document.querySelector('.card-container');
  const searchForm = document.querySelector('#search-form');
  let hasMore = true;
  let offset = 0;

  const ioOptions = {
    root: null,
    rootMargin: '200px 0px 0px 0px',
    threshold: 0.5,
  };

  const io = new IntersectionObserver(handleIntersection, ioOptions);
  io.observe(document.querySelector('footer'));

  searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    cardContainer.innerHTML = '';
    getFilteredModels(offset);
  });

  function handleIntersection(enteries) {
    if (enteries[0].isIntersecting) {
      if (hasMore) {
        setTimeout(() => {
          getFilteredModels(offset);
        }, 250);
      }
    }
  }

  async function getFilteredModels(nextSet) {
    const country = document.querySelector<HTMLSelectElement>('#id_country').selectedOptions[0].text;
    // @ts-ignore
    const city = document.getElementById('id_city').value;
    // @ts-ignore
    const gender = document.getElementById('id_gender').value;
    // @ts-ignore
    const hair = document.getElementById('id_hair').value;
    // @ts-ignore
    const eyes = document.getElementById('id_eyes').value;
    // @ts-ignore
    const height = document.getElementById('id_height').value;
    const searchParams = `country=${country}&city=${city}&gender=${gender}&hair=${hair}&eyes=${eyes}&height=${height}`;

    try {
      const { data } = await http.get(
        `models/search/?${searchParams}&offset=${nextSet}`
      );

      // If we get no data stop fetching
      if (data.next) {
        hasMore = true;
        const url = new URL(data.next);
        offset = parseInt(url.searchParams.get('offset'), 10);
      } else {
        offset = 0;
        hasMore = false;
      }

      data.results.forEach((model) => createCard(model, cardContainer));
    } catch (error) {
      // TODO(karim): remove this logs
      console.log(error);
      console.log(error.response);
    }
  }
});
