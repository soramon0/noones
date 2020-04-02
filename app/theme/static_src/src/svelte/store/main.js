import { writable } from 'svelte/store';
const { subscribe, set, update } = writable(null);

export default {
  subscribe,
  update,
  set,
  populate: async () => {
    const res = await fetch('/api/models/me');

    if (res.status === 401) {
      return window.location.replace('/');
    }

    const data = await res.json();

    set(data);
  }
};
