import { writable } from "svelte/store";
import http from "../../main/http";
import UIStore from "./ui";
import { onUploadProgress } from "./photo";

const GALLERYSIZELIMIT = 1024 * 1024 * 5; // 5MB

function validFileType(type = "") {
  return !type.startsWith("image/") ? false : true;
}

function validFileSize(fileSize, sizeLimit) {
  return fileSize > sizeLimit ? false : true;
}

const { subscribe, set, update } = writable({
  measures: {},
  measuresErrors: {},
  model: {},
  gallery: [],
  galleryErrors: {},
});

export default {
  subscribe,
  update,
  set,
  createMeasuresUpdate: async (payload) => {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      const { data } = await http.post(`update/measures/`, payload);
      // add errors object which will store errors
      // related to measures
      data.errors = {};

      update((store) => ({
        ...store,
        measures: data,
        measuresErrors: {},
      }));

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      update((store) => ({
        ...store,
        measuresErrors: response.data,
      }));
    }
  },
  modifyMeasuresUpdate: async (measures_id, payload) => {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      const { data } = await http.put(
        `update/measures/${measures_id}/`,
        payload
      );

      data.errors = {};

      update((store) => ({
        ...store,
        measures: data,
        measuresErrors: {},
      }));

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      // if we couldn't find an update with the given id
      // then it probably was removed by admin
      if (response && response.status === 404) {
        const errors = {
          measure: ["Update has been removed. Check your email for details."],
        };

        update((store) => ({
          ...store,
          measures: { ...store.measures, errors },
        }));
      }

      update((store) => ({
        ...store,
        measures: { ...store.measures, errors: response.data },
      }));
    }
  },
  getMeasuresUpdate: async (measureId) => {
    try {
      const { data } = await http.get(`update/measures/${measureId}/`);
      data.errors = {};
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
      UIStore.setFetchAndFeedbackModal(false, false);

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
            galleryErrors: {
              image: [`"${file.name}" is not an image`],
            },
          }));
          isValid = false;
          return;
        }
        if (!validFileSize(file.size, GALLERYSIZELIMIT)) {
          update((store) => ({
            ...store,
            galleryErrors: {
              image: [`"${file.name}" should not be greater than 5mb`],
            },
          }));
          isValid = false;
          return;
        }
        imageData.append("image", file);
      });

      if (!isValid) return;

      UIStore.setFetchAndFeedbackModal(true, false);
      const { data } = await http.post("update/gallery/", imageData, {
        onUploadProgress,
      });

      update((store) => {
        const { gallery } = store;

        gallery.unshift(...data);

        return { ...store, gallery };
      });

      UIStore.setFetchAndFeedbackModal(false, true);
      UIStore.setfileUploadPercentage(0);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);
      UIStore.setfileUploadPercentage(0);

      update((store) => ({ ...store, galleryErrors: response.data }));
    }
  },
  createOrModifyGalleryUpdate: async (file, photoId) => {
    try {
      if (!validFileType(file.type)) {
        update((store) => ({
          ...store,
          galleryErrors: {
            image: [`"${file.name}" is not an image`],
          },
        }));
        return;
      }
      if (!validFileSize(file.size, GALLERYSIZELIMIT)) {
        update((store) => ({
          ...store,
          galleryErrors: {
            image: [`"${file.name}" should not be greater than 5mb`],
          },
        }));
        return;
      }
      const imageData = new FormData();
      imageData.append("image", file);

      UIStore.setFetchAndFeedbackModal(true, false);
      const { status, data } = await http.put(
        `update/gallery/related_photo/${photoId}/`,
        imageData
      );

      update((store) => {
        const { gallery } = store;
        data.errors = {};

        if (status === 200) {
          const index = gallery.findIndex((photo) => photo.id === data.id);
          if (index != -1) {
            gallery[index] = data;
          }
        }

        if (status === 201) {
          gallery.unshift(data);
        }

        return { ...store, gallery };
      });

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      update((store) => ({ ...store, galleryErrors: response.data }));
    }
  },
  getGalleryUpdate: async () => {
    try {
      const { data } = await http.get("update/gallery/");
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
      imageData.append("image", file);

      const { data } = await http.put(`update/gallery/${photoId}/`, imageData);
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
          gallery[index]["errors"] = response.data;
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

      await http.delete(`update/gallery/${photoId}/`);

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
            measure: ["Update has been removed. Check your email for details."],
          };
          const index = gallery.findIndex((photo) => photo.id === photoId);

          if (index != -1) {
            gallery[index]["errors"] = errors;
          }

          return {
            ...store,
            gallery,
          };
        });
      }
    }
  },
  clearMeasuresErrors: () =>
    update((store) => ({ ...store, measuresErrors: {} })),
  clearMeasuresUpdateErrors: () => {
    update((store) => ({
      ...store,
      measures: { ...store.measures, errors: {} },
    }));
  },
  clearGalleryPhotoError: (index) => {
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
  clearGalleryError: () => update((store) => ({ ...store, galleryErrors: {} })),
};
