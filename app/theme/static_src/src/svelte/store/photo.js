import { writable } from "svelte/store";
import http from "../../main/http";
import UIStore from "./ui";
import UserStore from "./main";

const { subscribe, set, update } = writable({
  photos: [],
  cover: {
    data: [],
    next: null,
  },
  profile: {
    data: [],
    next: null,
  },
  errors: {},
});

export function onUploadProgress(progressEvent) {
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

  // if sizeLimit == 1 => 1mb || 2 => 2mb. etc
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
  getProfilePictures: async (cursor = "") => {
    try {
      const { data } = await http.get(`/models/photos/profile/?${cursor}`);
      let nextCursor = null;

      if (data.next) {
        nextCursor = data.next.split("?")[1];
      }

      // add errors object which will store errors
      // related to each photo entry
      const pictures = data.results.map((pic) => ({ ...pic, errors: {} }));

      update((store) => {
        return {
          ...store,
          profile: {
            data: [...store.profile.data, ...pictures],
            next: nextCursor,
          },
        };
      });
    } catch (_) {
      return;
    }
  },
  markProfilePicture: async (pictureId, pictureIndex) => {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      await http.put(`models/photos/profile/${pictureId}/mark/`);

      update((store) => {
        let { data, next } = store.profile;

        const oldPictureIndex = data.findIndex((photo) => photo.inUse);

        if (oldPictureIndex != -1) {
          data[oldPictureIndex].inUse = false;
        }

        if (data[pictureIndex] != undefined) {
          data[pictureIndex].inUse = true;
          UserStore.markAsProfilePicture(data[pictureIndex]);
        }

        return {
          ...store,
          profile: {
            next,
            data,
          },
        };
      });

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      update((store) => {
        store.errors["profilePicture"] = response.data["profilePicture"] || [
          response.data["detail"],
        ];

        return {
          ...store,
        };
      });
    }
  },
  deleteProfilePicture: async (id) => {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      await http.delete(`models/photos/profile/${id}/`);

      update((store) => {
        let { data, next } = store.profile;

        data = data.filter((photo) => photo.id != id);

        return {
          ...store,
          profile: {
            next,
            data,
          },
        };
      });

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      update((store) => {
        store.errors["profilePicture"] = response.data["profilePicture"] || [
          response.data["detail"],
        ];

        return {
          ...store,
        };
      });
    }
  },
  getCoverPictures: async (cursor = "") => {
    try {
      const { data } = await http.get(`/models/photos/cover/?${cursor}`);
      let nextCursor = null;

      if (data.next) {
        nextCursor = data.next.split("?")[1];
      }

      // add errors object which will store errors
      // related to each photo entry
      const pictures = data.results.map((pic) => ({ ...pic, errors: {} }));

      update((store) => {
        return {
          ...store,
          cover: {
            data: [...store.cover.data, ...pictures],
            next: nextCursor,
          },
        };
      });
    } catch (_) {
      return;
    }
  },
  markCoverPicture: async (pictureId, pictureIndex) => {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      await http.put(`models/photos/cover/${pictureId}/mark/`);

      update((store) => {
        let { data, next } = store.cover;

        const oldPictureIndex = data.findIndex((photo) => photo.inUse);

        if (oldPictureIndex != -1) {
          data[oldPictureIndex].inUse = false;
        }

        if (data[pictureIndex] != undefined) {
          data[pictureIndex].inUse = true;
          UserStore.markAsCoverPicture(data[pictureIndex]);
        }

        return {
          ...store,
          cover: {
            next,
            data,
          },
        };
      });

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      update((store) => {
        store.errors["coverPicture"] = response.data["coverPicture"] || [
          response.data["detail"],
        ];

        return {
          ...store,
        };
      });
    }
  },
  deleteCoverPicture: async (id) => {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      await http.delete(`models/photos/cover/${id}/`);

      update((store) => {
        let { data, next } = store.cover;

        data = data.filter((photo) => photo.id != id);

        return {
          ...store,
          cover: {
            next,
            data,
          },
        };
      });

      UIStore.setFetchAndFeedbackModal(false, true);
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      update((store) => {
        store.errors["coverPicture"] = response.data["coverPicture"] || [
          response.data["detail"],
        ];

        return {
          ...store,
        };
      });
    }
  },
  clearErrors: () => update((store) => ({ ...store, errors: {} })),
};
