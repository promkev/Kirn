import UserSession from "../Models/UserSession";
import appwrite from "../Constants/Appwrite";

export default async function LoggedIn(): Promise<UserSession> {
  var session: UserSession = {
    $id: "",
    name: "",
    registration: 0,
    status: 0,
    passwordUpdate: 0,
    email: "",
    emailVerification: false,
    prefs: {},
  };
  await appwrite.account.get<UserSession>().then(
    function (response) {
      session = response;
    },
    function (error) {
      console.log("User not found");
    }
  );
  return session;
}
