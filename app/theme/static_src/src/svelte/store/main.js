import { writable } from 'svelte/store';
const { subscribe, set, update } = writable(null);

export default {
  subscribe,
  update,
  set,
  // increment: () => update(n => n + 1),
  // decrement: () => update(n => n - 1),
  reset: () => set({}),
  populate: async () => {
    const res = await fetch('/api/models/me');

    if (!res.ok) {
      window.location.replace('/');
    }

    const data = await res.json();
    const modelData = data && JSON.parse(data.model);
    const model = modelData
      ? { id: modelData[0].pk, ...modelData[0].fields, email: data.email }
      : {};

    set(model);
  }
};
