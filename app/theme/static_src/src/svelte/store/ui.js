import { writable } from 'svelte/store';

const { subscribe, set, update } = writable({
  fetching: false,
  success: false,
});

export default {
  subscribe,
  update,
  set,
  setFetching: (fetching) => update(({ success }) => ({ fetching, success })),
  setSuccess: (success) => update(({ fetching }) => ({ fetching, success })),
  setFetchAndSuccess: (fetching, success) =>
    update(() => ({ fetching, success })),
};
