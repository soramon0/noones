import { writable } from "svelte/store";
import http from "../../main/http";
import UIStore from "./ui";

const { subscribe, set, update } = writable({
  photos: [],
  cover: null,
  profile: null,
  errors: {},
});

function onUploadProgress(progressEvent) {
  // look if lengthComputable, if not try and get the length from the header,
  // if not try and get the decompressed content length
  const totalLength = progressEvent.lengthComputable
    ? progressEvent.total
    : progressEvent.target.getResponseHeader("content-length") ||
      progressEvent.target.getResponseHeader("x-decompressed-content-length");

  if (totalLength != null) {
    const percentage = Math.round((progressEvent.loaded * 100) / totalLength);

    UIStore.setfileUploadPercentage(percentage);
  }
}

function fileIsValid(file, key, sizeLimit) {
  // TODO(kairm): check with project manager for supported mimetypes
  if (!file.type.startsWith("image/")) {
    update((store) => ({
      ...store,
      errors: {
        [key]: [`${file.name} is not an image`],
      },
    }));
    return false;
  }

  // if sizeLimit = 1 => 1mb || 2 => 2mb. etc
  const size = 1024 * 1024 * sizeLimit;
  if (file.size > size) {
    update((store) => ({
      ...store,
      errors: {
        [key]: [`${file.name} should not be greater than ${sizeLimit}mb`],
      },
    }));

    return false;
  }

  return true;
}

export default {
  subscribe,
  update,
  set,
  populate: (data) => update((store) => ({ ...store, ...data })),
  uploadProfilePicture: async (file) => {
    if (!fileIsValid(file, "profilePicture", 1)) {
      return;
    }

    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      // Create image data and send it
      const imageData = new FormData();
      imageData.append("profilePicture", file);

      const { data } = await http.put("/models/photos/profile/", imageData, {
        onUploadProgress,
      });

      // Update store with new image
      update((store) => ({
        ...store,
        errors: {},
        profile: data.profilePicture,
      }));

      UIStore.setFetchAndFeedbackModal(false, true);
      UIStore.setfileUploadPercentage(0);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);
      UIStore.setfileUploadPercentage(0);

      update((store) => ({ ...store, errors: response.data }));
    }
  },
  uploadCoverPicture: async (file) => {
    if (!fileIsValid(file, "coverPicture", 2)) {
      return;
    }

    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      // Create image data and send it
      const imageData = new FormData();
      imageData.append("coverPicture", file);

      const { data } = await http.put("/models/photos/cover/", imageData, {
        onUploadProgress,
      });

      // Update store with new image
      update((store) => ({
        ...store,
        errors: {},
        cover: data.coverPicture,
      }));

      UIStore.setFetchAndFeedbackModal(false, true);
      UIStore.setfileUploadPercentage(0);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);
      UIStore.setfileUploadPercentage(0);

      update((store) => ({ ...store, errors: response.data }));
    }
  },
  uploadGalleryPictures: async (files) => {
    let isValid = true;
    const imageData = new FormData();

    files.forEach((file) => {
      if (!fileIsValid(file, "image", 5)) {
        isValid = false;
        return;
      }
      imageData.append("image", file);
    });

    if (!isValid) {
      return;
    }

    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      const { data } = await http.post("/models/photos/gallery/", imageData, {
        onUploadProgress,
      });

      // Update store with new images
      update((store) => ({
        ...store,
        errors: {},
        photos: [...store.photos, ...data],
      }));

      UIStore.setFetchAndFeedbackModal(false, true);
      UIStore.setfileUploadPercentage(0);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);
      UIStore.setfileUploadPercentage(0);

      update((store) => ({ ...store, errors: response.data }));
    }
  },
  updateGalleryPicture: async (file, id, modelId) => {
    if (!fileIsValid(file, "image", 5)) {
      return;
    }

    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      // Create image data and send it
      const imageData = new FormData();
      imageData.append("image", file);
      imageData.append('model', modelId)

      const { data } = await http.put(`/models/photos/gallery/${id}`, imageData);

      // Update store with new image
      update((store) => {
        const { photos } = store
        const index = photos.findIndex(photo => photo.id === id)
        photos[index] = data

        return {
          ...store,
          errors: {},
          photos: photos,
        }
      });

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      update((store) => ({ ...store, errors: response.data }));
    }
  }
};
