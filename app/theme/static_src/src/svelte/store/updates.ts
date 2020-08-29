import { writable } from 'svelte/store';
import http from '../../main/http';
import UIStore from './ui';
import { onUploadProgress } from './photo';
import type {
  IProfileUpdate,
  IMeasureseUpdate,
  IProfilePictureeUpdate,
  ICoverPictureUpdate,
  IGallaryUpdate,
  IMeasures,
} from '../types/models';

const GALLERYSIZELIMIT = 1024 * 1024 * 5; // 5MB
const PROFILEPICSIZELIMIT = 1024 * 1024 * 3; // 3MB

function validFileType(type = '') {
  return !type.startsWith('image/') ? false : true;
}

function validFileSize(fileSize, sizeLimit) {
  return fileSize > sizeLimit ? false : true;
}

type ProfileUpdates = {
  model: IProfileUpdate;
  measures: IMeasureseUpdate;
  profilePictures: IProfilePictureeUpdate[];
  coverPictures: ICoverPictureUpdate[];
  gallery: IGallaryUpdate[];
  errors: any;
};

// TODO(karim): fix error handling for profile
const { subscribe, set, update } = writable<ProfileUpdates>({
  model: {} as IProfileUpdate,
  measures: {} as IMeasureseUpdate,
  profilePictures: [],
  coverPictures: [],
  gallery: [],
  errors: {},
});

export default {
  subscribe,
  update,
  set,
  async createProfileUpdate(bio: string) {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      const { data } = await http.post<IProfileUpdate>(`update/profile/`, {
        bio,
      });

      // Add a errors objects to the data. It can be
      // used to display errors specific to this update.
      data.errors = {};

      update((store) => ({
        ...store,
        model: data,
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
  async modifyProfileUpdate(updateId: string, payload: IProfileUpdate) {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      const { data } = await http.put<IProfileUpdate>(
        `update/profile/${updateId}/`,
        payload
      );

      data.errors = {};

      update((store) => ({
        ...store,
        model: data,
      }));

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      // if we couldn't find an update with the given id
      // then it probably was removed by admin
      if (response?.status === 404) {
        const errors = {
          model: ['Update has been removed.'],
        };

        update((store) => ({
          ...store,
          model: { ...store.model, errors },
        }));
      } else {
        update((store) => ({
          ...store,
          model: { ...store.model, errors: response.data },
        }));
      }
    }
  },
  async getProfileUpdate() {
    try {
      const { data } = await http.get<IProfileUpdate>(`update/profile/`);
      data.errors = {};
      update((store) => ({ ...store, model: data }));
    } catch (_) {
      return;
    }
  },
  async deleteProfileUpdate(updateId: string) {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      await http.delete(`update/profile/${updateId}/`);
      update((store) => ({
        ...store,
        model: {} as IProfileUpdate,
      }));

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      // if we couldn't find an update with the given id
      // then it probably was removed by admin
      if (response?.status === 404) {
        const errors = {
          model: ['Update has been removed.'],
        };

        update((store) => ({
          ...store,
          errors,
          model: {} as IProfileUpdate,
        }));
      } else {
        update((store) => ({
          ...store,
          errors: response?.data,
          model: {} as IProfileUpdate,
        }));
      }
    }
  },
  createMeasuresUpdate: async (payload: IMeasures) => {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      const { data } = await http.post<IMeasureseUpdate>(
        `update/measures/`,
        payload
      );
      // add errors object which will store errors
      // related to measures
      data.errors = {};

      update((store) => ({
        ...store,
        measures: data,
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
  modifyMeasuresUpdate: async (updateId: string, payload: IMeasureseUpdate) => {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      const { data } = await http.put<IMeasureseUpdate>(
        `update/measures/${updateId}/`,
        payload
      );

      data.errors = {};

      update((store) => ({
        ...store,
        measures: data,
        errors: {},
      }));

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      // if we couldn't find an update with the given id
      // then it probably was removed by admin
      if (response?.status === 404) {
        const errors = {
          measures: ['Update has been removed.'],
        };

        update((store) => ({
          ...store,
          measures: { ...store.measures, errors },
        }));
      } else {
        update((store) => ({
          ...store,
          measures: { ...store.measures, errors: response.data },
        }));
      }
    }
  },
  getMeasuresUpdate: async () => {
    try {
      const { data } = await http.get<IMeasureseUpdate>(`update/measures/`);
      data.errors = {};
      update((store) => ({ ...store, measures: data }));
    } catch (_) {
      return;
    }
  },
  deleteMeasuresUpdate: async (updateId: string) => {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      await http.delete(`update/measures/${updateId}/`);
      update((store) => ({ ...store, measures: {} as IMeasureseUpdate }));

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      // if we couldn't find an update with the given id
      // then it probably was removed by admin
      if (response?.status === 404) {
        const errors = {
          measures: ['Update has been removed.'],
        };
        update((store) => ({
          ...store,
          measures: {} as IMeasureseUpdate,
          errors,
        }));
      } else {
        update((store) => ({
          ...store,
          errors: response?.data,
          measures: {} as IMeasureseUpdate,
        }));
      }
    }
  },
  createProfilePictureUpdate: async (file) => {
    try {
      if (!validFileType(file.type)) {
        update((store) => ({
          ...store,
          errors: {
            profilePicture: [`"${file.name}" is not an image`],
          },
        }));
        return;
      }
      if (!validFileSize(file.size, PROFILEPICSIZELIMIT)) {
        update((store) => ({
          ...store,
          errors: {
            profilePicture: [`"${file.name}" should not be greater than 3mb`],
          },
        }));
        return;
      }
      const imageData = new FormData();
      imageData.append('image', file);

      UIStore.setFetchAndFeedbackModal(true, false);

      const { data } = await http.post(`update/photos/profile/`, imageData);
      data.errors = {};

      update((store) => {
        const { profilePictures } = store;

        profilePictures.unshift(data);

        return { ...store, profilePictures, errors: {} };
      });

      UIStore.setFetchAndFeedbackModal(false, true);
      UIStore.setfileUploadPercentage(0);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);
      UIStore.setfileUploadPercentage(0);

      update((store) => ({
        ...store,
        errors: { profilePicture: response.data },
      }));
    }
  },
  getProfilePicturesUpdate: async () => {
    try {
      const { data } = await http.get('update/photos/profile/');
      // add errors object which will store errors
      // related to each photo entry
      const pictures = data.map((pic) => ({ ...pic, errors: {} })).reverse();
      update((store) => ({ ...store, profilePictures: pictures }));
    } catch (_) {
      return;
    }
  },
  modifyProfilePictureUpdate: async (file, photoId) => {
    try {
      if (!validFileType(file.type)) {
        update((store) => {
          const { profilePictures } = store;
          const index = profilePictures.findIndex(
            (photo) => photo.id === photoId
          );
          if (index != -1) {
            profilePictures[index].errors = {
              image: [`"${file.name}" is not an image`],
            };
          }
          return {
            ...store,
            profilePictures,
          };
        });
        return;
      }
      if (!validFileSize(file.size, PROFILEPICSIZELIMIT)) {
        update((store) => {
          const { profilePictures } = store;
          const index = profilePictures.findIndex(
            (photo) => photo.id === photoId
          );
          if (index != -1) {
            profilePictures[index].errors = {
              image: [`"${file.name}" should not be greater than 3mb`],
            };
          }
          return {
            ...store,
            profilePictures,
          };
        });
        return;
      }

      UIStore.setFetchAndFeedbackModal(true, false);

      const imageData = new FormData();
      imageData.append('image', file);

      const { data } = await http.put(
        `update/photos/profile/${photoId}/`,
        imageData
      );
      data.errors = {};

      update((store) => {
        const { profilePictures } = store;
        const index = profilePictures.findIndex(
          (photo) => photo.id === photoId
        );

        if (index != -1) {
          profilePictures[index] = data;
        }

        return {
          ...store,
          profilePictures,
        };
      });

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      update((store) => {
        const { profilePictures } = store;
        const index = profilePictures.findIndex(
          (photo) => photo.id === photoId
        );

        if (index != -1) {
          profilePictures[index]['errors'] = response.data;
        }

        return {
          ...store,
          profilePictures,
        };
      });
    }
  },
  deleteProfilePictureUpdate: async (photoId: string) => {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      await http.delete(`update/photos/profile/${photoId}/`);

      update((store) => {
        let { profilePictures } = store;

        profilePictures = profilePictures.filter(
          (photo) => photo.id != photoId
        );

        return { ...store, profilePictures };
      });

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      // if we couldn't find an update with the given id
      // then it probably was removed by admin
      if (response && response.status === 404) {
        update((store) => {
          const { profilePictures } = store;
          const errors = {
            image: ['Update has been removed.'],
          };
          const index = profilePictures.findIndex(
            (photo) => photo.id === photoId
          );

          if (index != -1) {
            profilePictures[index]['errors'] = errors;
          }

          return {
            ...store,
            profilePictures,
          };
        });
      }
    }
  },
  createCoverPictureUpdate: async (file) => {
    try {
      if (!validFileType(file.type)) {
        return update((store) => ({
          ...store,
          errors: {
            coverPicture: [`"${file.name}" is not an image`],
          },
        }));
      }
      if (!validFileSize(file.size, PROFILEPICSIZELIMIT)) {
        return update((store) => ({
          ...store,
          errors: {
            coverPicture: [`"${file.name}" should not be greater than 3mb`],
          },
        }));
      }
      const imageData = new FormData();
      imageData.append('image', file);

      UIStore.setFetchAndFeedbackModal(true, false);

      const { data } = await http.post(`update/photos/cover/`, imageData);
      data.errors = {};

      update((store) => {
        const { coverPictures } = store;

        coverPictures.unshift(data);

        return { ...store, coverPictures, errors: {} };
      });

      UIStore.setFetchAndFeedbackModal(false, true);
      UIStore.setfileUploadPercentage(0);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);
      UIStore.setfileUploadPercentage(0);

      update((store) => ({
        ...store,
        errors: { coverPictures: response.data },
      }));
    }
  },
  getCoverPictureUpdate: async () => {
    try {
      const { data } = await http.get('update/photos/cover/');
      // add errors object which will store errors
      // related to each photo entry
      const pictures = data.map((pic) => ({ ...pic, errors: {} })).reverse();
      update((store) => ({ ...store, coverPictures: pictures }));
    } catch (_) {
      return;
    }
  },
  modifyCoverPictureUpdate: async (file, photoId) => {
    try {
      if (!validFileType(file.type)) {
        update((store) => {
          const { coverPictures } = store;
          const index = coverPictures.findIndex(
            (photo) => photo.id === photoId
          );
          if (index != -1) {
            coverPictures[index].errors = {
              image: [`"${file.name}" is not an image`],
            };
          }
          return {
            ...store,
            coverPictures,
          };
        });
        return;
      }
      if (!validFileSize(file.size, PROFILEPICSIZELIMIT)) {
        update((store) => {
          const { coverPictures } = store;
          const index = coverPictures.findIndex(
            (photo) => photo.id === photoId
          );
          if (index != -1) {
            coverPictures[index].errors = {
              image: [`"${file.name}" should not be greater than 3mb`],
            };
          }
          return {
            ...store,
            coverPictures,
          };
        });
        return;
      }

      UIStore.setFetchAndFeedbackModal(true, false);

      const imageData = new FormData();
      imageData.append('image', file);

      const { data } = await http.put(
        `update/photos/cover/${photoId}/`,
        imageData
      );
      data.errors = {};

      update((store) => {
        const { coverPictures } = store;
        const index = coverPictures.findIndex((photo) => photo.id === photoId);

        if (index != -1) {
          coverPictures[index] = data;
        }

        return {
          ...store,
          coverPictures,
        };
      });

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      update((store) => {
        const { coverPictures } = store;
        const index = coverPictures.findIndex((photo) => photo.id === photoId);

        if (index != -1) {
          coverPictures[index]['errors'] = response.data;
        }

        return {
          ...store,
          coverPictures,
        };
      });
    }
  },
  deleteCoverPictureUpdate: async (photoId) => {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      await http.delete(`update/photos/cover/${photoId}/`);

      update((store) => {
        let { coverPictures } = store;

        coverPictures = coverPictures.filter((photo) => photo.id != photoId);

        return { ...store, coverPictures };
      });

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      // if we couldn't find an update with the given id
      // then it probably was removed by admin
      if (response && response.status === 404) {
        update((store) => {
          const { coverPictures } = store;
          const errors = {
            image: ['Update has been removed.'],
          };
          const index = coverPictures.findIndex(
            (photo) => photo.id === photoId
          );

          if (index != -1) {
            coverPictures[index]['errors'] = errors;
          }

          return {
            ...store,
            coverPictures,
          };
        });
      }
    }
  },
  createGallaryPhotoUpdate: async (files) => {
    try {
      const imageData = new FormData();
      let isValid = true;

      files.forEach((file) => {
        if (!validFileType(file.type)) {
          update((store) => ({
            ...store,
            errors: {
              gallery: [`"${file.name}" is not an image`],
            },
          }));
          isValid = false;
          return;
        }
        if (!validFileSize(file.size, GALLERYSIZELIMIT)) {
          update((store) => ({
            ...store,
            errors: {
              gallery: [`"${file.name}" should not be greater than 5mb`],
            },
          }));
          isValid = false;
          return;
        }
        imageData.append('image', file);
      });

      if (!isValid) return;

      UIStore.setFetchAndFeedbackModal(true, false);

      let { data } = await http.post(`update/photos/gallery/`, imageData, {
        onUploadProgress,
      });

      data = data.map((el) => ({ ...el, errors: {} })).reverse();

      update((store) => {
        const { gallery } = store;

        gallery.unshift(...data);

        return { ...store, gallery, errors: {} };
      });

      UIStore.setFetchAndFeedbackModal(false, true);
      UIStore.setfileUploadPercentage(0);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);
      UIStore.setfileUploadPercentage(0);

      update((store) => ({ ...store, errors: { ...response.data } }));
    }
  },
  createOrModifyGalleryUpdate: async (file, photoId) => {
    try {
      if (!validFileType(file.type)) {
        update((store) => ({
          ...store,
          errors: {
            galleryUpdate: [`"${file.name}" is not an image`],
          },
        }));
        return;
      }
      if (!validFileSize(file.size, GALLERYSIZELIMIT)) {
        update((store) => ({
          ...store,
          errors: {
            galleryUpdate: [`"${file.name}" should not be greater than 5mb`],
          },
        }));
        return;
      }
      const imageData = new FormData();
      imageData.append('image', file);

      UIStore.setFetchAndFeedbackModal(true, false);
      const { status, data } = await http.put(
        `update/photos/gallery/related_photo/${photoId}/`,
        imageData
      );

      update((store) => {
        const { gallery } = store;
        data.errors = {};

        // Ok response means we modified an existing update
        if (status === 200) {
          const index = gallery.findIndex((photo) => photo.id === data.id);
          if (index != -1) {
            gallery[index] = data;
          }
        }

        // Newly CREATED
        if (status === 201) {
          gallery.unshift(data);
        }

        return { ...store, gallery };
      });

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      update((store) => ({
        ...store,
        errors: { galleryUpdate: response.data },
      }));
    }
  },
  getGalleryUpdate: async () => {
    try {
      const { data } = await http.get('update/photos/gallery/');
      // add errors object which will store errors
      // related to each photo entry
      const gallery = data.map((el) => ({ ...el, errors: {} })).reverse();
      update((store) => ({ ...store, gallery }));
    } catch (_) {
      return;
    }
  },
  modifyGalleryPhotoUpdate: async (file, photoId) => {
    try {
      if (!validFileType(file.type)) {
        update((store) => {
          const { gallery } = store;
          const index = gallery.findIndex((photo) => photo.id === photoId);
          if (index != -1) {
            gallery[index].errors = {
              image: [`"${file.name}" is not an image`],
            };
          }
          return {
            ...store,
            gallery,
          };
        });
        return;
      }
      if (!validFileSize(file.size, GALLERYSIZELIMIT)) {
        update((store) => {
          const { gallery } = store;
          const index = gallery.findIndex((photo) => photo.id === photoId);
          if (index != -1) {
            gallery[index].errors = {
              image: [`"${file.name}" should not be greater than 5mb`],
            };
          }
          return {
            ...store,
            gallery,
          };
        });
        return;
      }

      UIStore.setFetchAndFeedbackModal(true, false);

      const imageData = new FormData();
      imageData.append('image', file);

      const { data } = await http.put(
        `update/photos/gallery/${photoId}/`,
        imageData
      );
      data.errors = {};

      update((store) => {
        const { gallery } = store;
        const index = gallery.findIndex((photo) => photo.id === photoId);

        if (index != -1) {
          gallery[index] = data;
        }

        return {
          ...store,
          gallery,
        };
      });

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      update((store) => {
        const { gallery } = store;
        const index = gallery.findIndex((photo) => photo.id === photoId);

        if (index != -1) {
          gallery[index]['errors'] = response.data;
        }

        return {
          ...store,
          gallery,
        };
      });
    }
  },
  deleteGalleryPhotoUpdate: async (photoId) => {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      await http.delete(`update/photos/gallery/${photoId}/`);

      update((store) => {
        let { gallery } = store;

        gallery = gallery.filter((photo) => photo.id != photoId);

        return { ...store, gallery };
      });

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      // if we couldn't find an update with the given id
      // then it probably was removed by admin
      if (response && response.status === 404) {
        update((store) => {
          const { gallery } = store;
          const errors = {
            image: ['Update has been removed.'],
          };
          const index = gallery.findIndex((photo) => photo.id === photoId);

          if (index != -1) {
            gallery[index]['errors'] = errors;
          }

          return {
            ...store,
            gallery,
          };
        });
      }
    }
  },
  clearProfileUpdateErrors: () => {
    update((store) => ({
      ...store,
      model: { ...store.model, errors: {} },
    }));
  },
  clearMeasuresUpdateErrors: () => {
    update((store) => ({
      ...store,
      measures: { ...store.measures, errors: {} },
    }));
  },
  clearGalleryPhotoErrors: (index) => {
    update((store) => {
      const { gallery } = store;
      const errors = gallery[index].errors;

      if (errors && Object.keys(errors).length > 0) {
        gallery[index].errors = {};
      }

      return {
        ...store,
        gallery,
      };
    });
  },
  clearProfilePictureErrors: (index) => {
    update((store) => {
      const { profilePictures } = store;
      const errors = profilePictures[index].errors;

      if (errors && Object.keys(errors).length > 0) {
        profilePictures[index].errors = {};
      }

      return {
        ...store,
        profilePictures,
      };
    });
  },
  clearCoverPictureErrors: (index) => {
    update((store) => {
      const { coverPictures } = store;
      const errors = coverPictures[index].errors;

      if (errors && Object.keys(errors).length > 0) {
        coverPictures[index].errors = {};
      }

      return {
        ...store,
        coverPictures,
      };
    });
  },
  clearErrors: (key) => {
    update((store) => {
      const { errors } = store;

      if (errors[key] && errors[key].length > 0) {
        errors[key] = [];
      }

      return { ...store, errors };
    });
  },
};
