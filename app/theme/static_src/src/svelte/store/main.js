import { writable } from 'svelte/store';
import http from '../../main/http';

const { subscribe, set, update } = writable(null);

export default {
  subscribe,
  update,
  set,
  populate: async () => {
    try {
      const { data } = await http.get(`/models/me/`);

      // Shaping the store data
      data.response = {
        fetching: false,
        success: false,
      };
      data.errors = {};
      data.cover = data.model.coverPicture;
      data.profile = data.model.profilePicture;

      set(data);
    } catch ({ response }) {
      if (response && response.status == 401) {
        window.location.replace('/');
      }
    }
  },
  updateModel: async (payload) => {
    try {
      update((store) => ({
        ...store,
        response: { success: false, fetching: true },
      }));

      const { data } = await http.put(`/models/${payload.id}/`, payload);

      update((store) => ({
        ...store,
        model: data,
        response: { fetching: false, success: true },
        errors: {},
      }));
    } catch ({ response }) {
      update((store) => ({
        ...store,
        errors: response.data,
        response: { fetching: false, success: false },
      }));
    }
  },
  updateMeasures: async (payload) => {
    try {
      update((store) => ({
        ...store,
        response: { success: false, fetching: true },
      }));

      const { data } = await http.put(`/measures/${payload.id}/`, payload);

      update((store) => ({
        ...store,
        measures: data,
        response: { success: true, fetching: false },
        errors: {},
      }));
    } catch ({ response }) {
      update((store) => ({
        ...store,
        errors: response.data,
        response: { success: false, fetching: false },
      }));
    }
  },
  setSuccess: (success) =>
    update((store) => ({ ...store, response: { fetching: false, success } })),
};
