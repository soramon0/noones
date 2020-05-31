import { writable } from "svelte/store";
import http from "../../main/http";
import UIStore from "./ui";

const { subscribe, set, update } = writable({
  measures: {},
  model: {},
  photos: {},
  errors: {},
});

export default {
  subscribe,
  update,
  set,
  createMeasuresUpdate: async (payload) => {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      const { data } = await http.post(`update/measures/`, payload);

      update((store) => ({
        ...store,
        measures: data,
        errors: {},
      }));

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      update((store) => ({
        ...store,
        errors: response.data,
      }));

      UIStore.setFetchAndFeedbackModal(false, false);
    }
  },
  updateMeasures: async (measures_id, payload) => {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      const { data } = await http.put(
        `update/measures/${measures_id}/`,
        payload
      );

      update((store) => ({
        ...store,
        measures: data,
        errors: {},
      }));

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      // if we couldn't find an update with the given id
      // then it probably was removed by admin
      if (response && response.status === 404) {
        update((store) => ({
          ...store,
          measures: {},
          errors: {
            measure: ["Update has been removed. Check your email for details."],
          },
        }));
      }

      update((store) => ({
        ...store,
        errors: response.data,
      }));

      UIStore.setFetchAndFeedbackModal(false, false);
    }
  },
  getMeasures: async (measureId) => {
    try {
      const { data } = await http.get(`update/measures/${measureId}/`);
      update((store) => ({ ...store, measures: data }));
    } catch (_) {
      return;
    }
  },
  deleteMeasuresUpdate: async (measureId) => {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      await http.delete(`update/measures/${measureId}/`);
      update((store) => ({ ...store, measures: {} }));

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      // if we couldn't find an update with the given id
      // then it probably was removed by admin
      if (response && response.status === 404) {
        update((store) => ({
          ...store,
          measures: {},
          errors: {
            measure: ["Update has been removed. Check your email for details."],
          },
        }));
      }
      UIStore.setFetchAndFeedbackModal(false, false);
    }
  },
};
