export default interface UserSession {
  $id: string;
  name: string;
  registration: number;
  status: number;
  passwordUpdate: number;
  email: string;
  emailVerification: boolean;
  prefs: Prefs;
}
export interface Prefs {}
