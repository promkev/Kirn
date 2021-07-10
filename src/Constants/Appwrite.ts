import { Appwrite } from "appwrite";

const appwrite = new Appwrite();
appwrite
  .setEndpoint("https://appwrite.grypr.cf/v1")
  .setProject("60e901305cf0c");

export default appwrite;
