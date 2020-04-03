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
      data.errors = {};

      set(data);
    } catch ({ response }) {
      if (response && response.status == 401) {
        window.location.replace('/');
      }
    }
  },
  updateModel: async (payload) => {
    try {
      const { data } = await http.put(`/models/${payload.id}/`, payload);
      update((store) => ({ ...store, model: data, errors: {} }));
    } catch ({ response }) {
      update((store) => ({ ...store, errors: response.data }));
    }
  },
  updateMeasures: async (payload) => {
    try {
      const { data } = await http.put(`/measures/${payload.id}/`, payload);
      update((store) => ({ ...store, measures: data, errors: {} }));
    } catch ({ response }) {
      update((store) => ({ ...store, errors: response.data }));
    }
  },
};
