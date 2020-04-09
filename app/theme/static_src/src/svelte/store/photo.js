import { writable } from 'svelte/store';

const { subscribe, set, update } = writable({
  photos: [],
  cover: null,
  profile: null,
});

export default {
  subscribe,
  update,
  set,
  populate: (data) => update(store => ({ ...store, ...data })),
};
