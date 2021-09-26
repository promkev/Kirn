import UserSession from "../Models/UserSession";
import appwrite from "../Constants/Appwrite";
import GetUserSession from "./GetUserSession";
import JoinCourseObject from "../Models/JoinCourseObject";
import ExecutionObject from "../Models/ExecutionObject";
import delay from "./Delay";

export default async function CreateExecution(
  courseName: string,
  guildId: string
): Promise<JoinCourseObject | void> {
  var response: JoinCourseObject = {
    success: false,
    code: -1,
    extra: "",
  };
  var loggedIn: Boolean = false;

  var resp: UserSession = await GetUserSession();
  if (resp.$id !== "") {
    loggedIn = true;
  }

  var execution: ExecutionObject;
  var functionId: string = "60ea1071cb1da";

  if (loggedIn === true) {
    execution = await appwrite.functions.createExecution(
      functionId,
      JSON.stringify({
        courseName: courseName,
        guildId: guildId,
      })
    );
  } else {
    return;
  }

  var status: string = "processing";
  while (status !== "completed") {
    await delay(250);
    execution = await appwrite.functions.getExecution(
      functionId,
      execution.$id
    );
    status = execution.status;
    console.log(execution);
  }
  console.log(execution.stdout);
  response = JSON.parse(execution.stdout);

  return response;
}
