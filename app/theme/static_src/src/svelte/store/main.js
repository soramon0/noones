import { writable } from 'svelte/store';
import http from '../../main/http';
import uiStore from './ui';
import photosStore from './photo'

const { subscribe, set, update } = writable(null);

export default {
  subscribe,
  update,
  set,
  populate: async () => {
    try {
      const { data } = await http.get(`models/me/`);

      // Shaping the store data
      data.errors = {};
      data.email = data.model.email;

      // create the photos' store
      const { coverPicture, profilePicture } = data.model
      photosStore.populate({ photos: data.photos, cover: coverPicture, profile: profilePicture })

      set(data);
    } catch ({ response }) {
      if (response && response.status == 401) {
        return window.location.replace('/');
      }
    }
  },
  updateModel: async (payload) => {
    try {
      uiStore.setFetchAndSuccess(true, false);

      const { data } = await http.put(`models/${payload.id}/`, payload);

      update((store) => ({
        ...store,
        model: data,
        errors: {},
      }));

      uiStore.setFetchAndSuccess(false, true);
    } catch ({ response }) {
      update((store) => ({
        ...store,
        errors: response.data,
      }));

      uiStore.setFetchAndSuccess(false, false);
    }
  },
  updateMeasures: async (payload) => {
    try {
      uiStore.setFetchAndSuccess(true, false);

      const { data } = await http.put(`models/measures/${payload.id}/`, payload);

      update((store) => ({
        ...store,
        measures: data,
        errors: {},
      }));

      uiStore.setFetchAndSuccess(false, true);
    } catch ({ response }) {
      update((store) => ({
        ...store,
        errors: response.data,
      }));

      uiStore.setFetchAndSuccess(false, false);
    }
  },
};
