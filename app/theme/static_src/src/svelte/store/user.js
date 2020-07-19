import { writable } from 'svelte/store';
import http from '../../main/http';
import UIStore from './ui';
import PhotosStore from './photo';

const { subscribe, set, update } = writable({
  model: {},
  measures: {},
  profilePicture: {},
  coverPicture: {},
  email: null,
  errors: {},
});

export default {
  subscribe,
  update,
  set,
  populate: async () => {
    try {
      const { data } = await http.get(`models/me/`);

      // create the photos' store
      PhotosStore.populate({ photos: data.photos });

      // Shaping the store data
      const { model, measures, profilePicture, coverPicture } = data;

      update((store) => ({
        ...store,
        model,
        measures,
        profilePicture,
        coverPicture,
        email: model.email,
      }));
    } catch ({ response }) {
      if (response && response.status == 401) {
        return window.location.replace('/');
      }

      throw response;
    }
  },
  async updateModel(payload) {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      const { data } = await http.patch(`models/${payload.id}/`, payload);

      update((store) => ({
        ...store,
        errors: {},
        model: data,
      }));

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      update((store) => ({
        ...store,
        errors: response.data,
      }));
    }
  },
  markAsProfilePicture: (data) =>
    update((store) => ({ ...store, profilePicture: data })),
  markAsCoverPicture: (data) =>
    update((store) => ({ ...store, coverPicture: data })),
  updatePassword: async (payload) => {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      await http.patch(`accounts/update-password/`, payload);

      update((store) => ({
        ...store,
        errors: {},
      }));

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      update((store) => ({
        ...store,
        errors: response.data,
      }));
    }
  },
};
