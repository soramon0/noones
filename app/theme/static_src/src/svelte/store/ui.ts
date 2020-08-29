import { writable } from "svelte/store";

const { subscribe, set, update } = writable({
  fetching: false,
  showFeedbackModal: false,
  fileUploadPercentage: 0,
});

export default {
  subscribe,
  update,
  set,
  setFetching: (fetching) => update((store) => ({ ...store, fetching })),
  setFeedbackModal: (showFeedbackModal) => update((store) => ({ ...store, showFeedbackModal })),
  setFetchAndFeedbackModal: (fetching, showFeedbackModal) =>
    update((store) => ({ ...store, fetching, showFeedbackModal })),
  setfileUploadPercentage: (percentage) =>
    update((store) => ({ ...store, fileUploadPercentage: percentage })),
};
