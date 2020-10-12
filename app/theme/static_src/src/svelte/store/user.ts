import { writable } from 'svelte/store';
import http from '../../main/http';
import PhotoStore from './photo';
import UIStore from './ui';
import type {
  IProfile,
  IMeasures,
  IProfilePicture,
  ICoverPicture,
  IGallary,
  ICountry,
  ICity
} from '../types/models';

type Profile = {
  model: IProfile;
  measures: IMeasures;
  email: string;
  profilePicture: IProfilePicture;
  coverPicture: ICoverPicture;
  countries: ICountry[],
  cities: ICity[],
  errors: any;
};

const { subscribe, set, update } = writable<Profile>({
  model: {} as IProfile,
  measures: {} as IMeasures,
  coverPicture: {} as ICoverPicture,
  profilePicture: {} as IProfilePicture,
  email: null,
  countries: [],
  cities: [],
  errors: {},
});

export default {
  subscribe,
  update,
  set,
  async populate() {
    try {
      // email and errors objects will not be in the response
      type MeResponse = Profile & {
        photos: IGallary;
      };

      const { data } = await http.get<MeResponse>(`models/me/`);

      // create the photos' store
      PhotoStore.populate({ photos: data.photos });

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
      throw response;
    }
  },
  async updateModel(payload) {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      const { data }: { data: IProfile } = await http.patch(
        `models/${payload.id}/`,
        payload
      );

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
  markAsProfilePicture(data: IProfilePicture) {
    update((store) => ({ ...store, profilePicture: data }));
  },
  markAsCoverPicture(data: ICoverPicture) {
    update((store) => ({ ...store, coverPicture: data }));
  },
  async changePassword(payload) {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      await http.patch(`accounts/update_password/`, payload);

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
  async changeEmail(email: string) {
    try {
      UIStore.setFetchAndFeedbackModal(true, false);

      await http.patch(`accounts/update_email/`, { email });

      update((store) => ({
        ...store,
        errors: {},
        email,
      }));

      UIStore.setFetchAndFeedbackModal(false, true);

      window.location.replace('/accounts/signin/');
    } catch ({ response }) {
      UIStore.setFetchAndFeedbackModal(false, false);

      update((store) => ({
        ...store,
        errors: response.data,
      }));
    }
  },
  async getCountries() {
    try {
      const { data } = await http.get<ICountry[]>('country/')
      update((store) => {
        return {
          ...store,
          countries: data
        }
      })
    } catch{}
  },
  async getCities(Countryname:string, countryCode: string) {
    try {
      const { data } = await http.get<ICity[]>('city/', {
        params: {
          country:Countryname,
          code:countryCode
        }
      })
      update((store) => {
        return {
          ...store,
          cities: data
        }
      })
    } catch{}
  }
};
