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

    setTimeout(() => {
      UIStore.setfileUploadPercentage(0);
      UIStore.setFetchAndSuccess(false, false);
    }, 1500);
  }
}

function fileIsValid(file) {
  // TODO(kairm): check with project manager for supported mimetypes
  if (!file.type.startsWith("image/")) {
    update((store) => ({
      ...store,
      errors: { profilePicture: ["selected file is not an image"] },
    }));
    return false;
  }

  // 1mb limit for profile picture
  if (file.size > 1000000) {
    update((store) => ({
      ...store,
      errors: {
        profilePicture: ["profile image should not be greater than 1mb"],
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
    if (!fileIsValid(file)) {
      return;
    }

    try {
      UIStore.setFetchAndSuccess(true, false);

      // Create image data and send it
      const imageData = new FormData();
      imageData.append("profilePicture", file);

      const { data } = await http.put("/models/picture/profile/", imageData, {
        onUploadProgress,
      });

      // Update store with new image
      update((store) => ({
        ...store,
        errors: {},
        profile: data.profilePicture,
      }));

      UIStore.setFetchAndSuccess(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndSuccess(false, false);

      update((store) => ({ ...store, errors: response.data }));
    }
  },
};
