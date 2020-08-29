export type ServerErrorResponse = {
  [key: string]: string[];
};

export interface IProfile {
  id: string;
  gender: string;
  first_name: string;
  last_name: string;
  bio?: string;
  birth_date: string;
  facebook: string;
  instagram: string;
  phone: string;
  address: string;
  city: string;
  country: string;
  zipcode: string;
  nin: string;
  email: string;
  user: string;
}

export interface IProfileUpdate {
  id: string;
  bio: string;
  accept: boolean | null;
  decline: boolean | null;
  message: string;
  errors: ServerErrorResponse;
}

export interface IMeasures {
  id: string;
  height: number;
  waist: number;
  bust: number;
  shoulders: number;
  hips: number;
  weight: number;
  shoe_size: number;
  hair: string;
  eyes: string;
}

export interface IMeasureseUpdate {
  id: string;
  height: number;
  waist: number;
  bust: number;
  shoulders: number;
  hips: number;
  weight: number;
  shoe_size: number;
  hair: string;
  eyes: string;
  accept: boolean | null;
  decline: boolean | null;
  message: string;
  errors: ServerErrorResponse;
}

export interface IProfilePicture {
  id: string;
  image: string;
  inUse: boolean;
  errors: ServerErrorResponse;
}

export interface IProfilePictureeUpdate {
  id: string;
  image: string;
  accept: boolean | null;
  decline: boolean | null;
  message: string;
  errors: ServerErrorResponse;
}

export interface ICoverPicture {
  id: string;
  image: string;
  inUse: boolean;
  errors: ServerErrorResponse;
}

export interface ICoverPictureUpdate {
  id: string;
  image: string;
  accept: boolean | null;
  decline: boolean | null;
  message: string;
  errors: ServerErrorResponse;
}

export interface IGallary {
  id: string;
  image: string;
  profile: string;
  errors: ServerErrorResponse;
}

export interface IGallaryUpdate {
  id: string;
  image: string;
  profile: string;
  accept: boolean | null;
  decline: boolean | null;
  message: string;
  related_photo: string;
  errors: ServerErrorResponse;
}
