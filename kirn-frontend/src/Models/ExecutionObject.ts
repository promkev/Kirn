export default interface ExecutionObject {
  $id: string;
  functionId: string;
  dateCreated: number;
  trigger: string;
  status: string;
  exitCode: number;
  stdout: string;
  stderr: string;
  time: number;
}
export interface Prefs {}
