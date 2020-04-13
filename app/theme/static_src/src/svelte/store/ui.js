import { writable } from "svelte/store";

const { subscribe, set, update } = writable({
  fetching: false,
  success: false,
  fileUploadPercentage: 0,
});

export default {
  subscribe,
  update,
  set,
  setFetching: (fetching) => update((store) => ({ ...store, fetching })),
  setSuccess: (success) => update((store) => ({ ...store, success })),
  setFetchAndSuccess: (fetching, success) =>
    update((store) => ({ ...store, fetching, success })),
  setfileUploadPercentage: (percentage) =>
    update((store) => ({ ...store, fileUploadPercentage: percentage })),
};
