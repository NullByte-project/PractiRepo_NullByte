export interface UserModel {
    id?: string;
    name: string;
    email: string;
    password: string;
}

export interface UserRegisterModel {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  role_id: string;
}