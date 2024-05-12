import { writable, type Writable } from "svelte/store";
import moment from "moment";

export type LoginBind = {
  emailInput: boolean;
  passwordInput: boolean;
};

export type SignUpBind = LoginBind & {
  fullNameInput: boolean;
  // instituteInput: boolean;
  cnfrmPasswordInput: boolean;
  employeeIDInput: boolean;
  unitInput: boolean;
  programInput: boolean;
};

export type Credentials = {
  deanInstitute: string;
  documentInstitute: string;
  program?: string;
  institute?: string;
  previlage?: string;
  email?: string;
  unit?: string;
  password?: string;
  btnDisabled?: boolean;
  userName?: string;
  cnfrmPassword?: string;
  captVerification?: boolean;
  captcha?: string;
  captchaID?: string | null;
  userImg?: string | null;
  fullName?: string;
  employeeID?: string;
  codeData?: string;
  documentName?: string;
  documentDescription?: string;
  documentProgram?: string;
  documentRegDate?: string;
  key?: string;
  full_ver_val?: boolean;
  approval?: string;
  edit?: boolean;
  comment?: string;
  count?: number;
};

export type RequestAPI = {
  method: string;
  address: string;
  credentials?: Credentials | undefined;
};

export type Route = {
  pathID: number;
  name: string;
  approved: boolean;
  processing: boolean;
  disapprovedDate: string;
  comment: string;
  approvedDate: string;
  confirmed: boolean;
  confirmedDate: string;
  finished: boolean;
  finishDate: string;
  complete: boolean;
  completeDate: string;
};

export type Document = {
  documentElement: any;
  body: any;
  attemps: number;
  documentID: number;
  codeData: string;
  documentName: string;
  documentDescription: string;
  pending: boolean;
  pendingDate: string;
  documentPath: Route[];
  notifications: Notification[];
};

export type Notification = {
  id: number;
  title: string;
  body: string;
  date: string;
};

export type Users = {
  institute: string;
  id?: number;
  previlage?: string;
  userImg: string;
  fullName?: string;
  user_name: string;
  email: string;
  employeeID?: string;
  unit?: string;
  full_ver_val?: boolean;
  registeredDate?: string;
  emailConfirmed?: boolean;
  open?: boolean;
  documents: Document[];
};

export type ResponseData = {
  error?: string;
  success?: string;
  remembered?: string;
  email?: string;
  user_name?: string;
  full_ver_val?: boolean;
  route?: string;
  captchaGETValue?: string[];
  captchaPOSTValue?: boolean;
  userImg?: string;
  fullName?: string;
  employeeID?: string;
  unit?: string;
  previlage?: string;
  notificationCount?: number;
  documents?: Document[];
  notifications?: Notification[];
  users?: Users[];
};

export const searchArray = (array: Document[], searchTerm: string) => {
  return array.filter((item) => {
    const lowerCasedSearchTerm = searchTerm.toLowerCase();

    // Customize the conditions based on your object properties
    return (
      item.documentName.toLowerCase().includes(lowerCasedSearchTerm) ||
      item.codeData.toLowerCase().includes(lowerCasedSearchTerm) ||
      item.pendingDate.toLowerCase().includes(lowerCasedSearchTerm) ||
      item.documentDescription.toLowerCase().includes(lowerCasedSearchTerm)
    );
  });
};

export const searchUser = (array: Users[], searchTerm: string) => {
  return array.filter((item) => {
    const lowerCasedSearchTerm = searchTerm.toLowerCase();

    // Customize the conditions based on your object properties
    return (
      item.email.toLowerCase().includes(lowerCasedSearchTerm) ||
      item.fullName.toLowerCase().includes(lowerCasedSearchTerm)
    );
  });
};

export const sortArray = (array: Document[], sortName: string): Document[] => {
  if (sortName === "Name") {
    return array.sort((a, b) => a.documentName.localeCompare(b.documentName));
  }

  if (sortName === "Date") {
    return array.sort(
      (a, b) =>
        moment(b.pendingDate).valueOf() - moment(a.pendingDate).valueOf()
    );
  }

  return array;
};

export const handleDetails = (
  userName: string,
  email: string,
  document: Document,
  confirmed?: string
) => {
  documentDetails.set({
    documentDetails: false,
    userNameD: userName,
    emailD: email,
    confirmedD: confirmed && confirmed.length ? confirmed.length : 0,
    documentD: document,
  });

  detailsExpand.set(true);
};

export const handleFetch = async (
  value: RequestAPI,
  token: null | string = ""
) => {
  const { method, address, credentials } = value;
  let request: any;

  if (method === "POST") {
    request = await handlePOST(address, credentials!, token);
  }

  if (method === "GET") {
    request = await handleGET(address, token);
  }

  if (request.ok) {
    return await request.json();
  } else {
    throw new Error(`Request failed with status ${request.status}`);
  }
};

const handlePOST = async (
  address: string,
  credentials: Credentials,
  token: null | string
) => {
  try {
    return await fetch(address, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token?.length && { Authorization: `Bearer ${token}` }),
      },
      body: JSON.stringify(credentials),
    });
  } catch (error) {
    showMessage.set({ error: "Server Unreachable" });
    console.error(error);
    throw error;
  }
};

const handleGET = async (address: string, token: null | string) => {
  try {
    return await fetch(address, {
      method: "GET",
      headers:
        token && token.length === 0
          ? {
              "Content-Type": "application/json",
            }
          : {
              Authorization: `Bearer ${token}`,
            },
    });
  } catch (error) {
    showMessage.set({ error: "Server Unreachable" });
    console.error(error);
    throw error;
  }
};

// export const address = "https://backend-tt9g.onrender.com";
export const address = "http://127.0.0.1:5000";

export const location = writable("/");
export const documentSelected = writable("");
export const appDate = writable("");
export const comDate = writable("");
export const activeTab = writable("Forward");
export const filterName = writable("All");

export const users: Writable<Users[]> = writable([]);
export const theDocument = writable({ name: "", id: "" });
export const showMessage: Writable<ResponseData> = writable({});
export const userData: Writable<ResponseData> = writable({});
export const documents: Writable<Document[]> = writable([]);
export const notifications: Writable<Notification[]> = writable([]);

export const documentDetails = writable({
  documentDetails: false,
  userNameD: "",
  emailD: "",
  confirmedD: 0,
  documentD: {},
});
// export const activeDocument = writable("");
// export const documentTimeZone = writable("");
export const notificationCount = writable(0);

localStorage.getItem("mode") || localStorage.setItem("mode", "System");
export const filterExpand = writable(false);
export const modeExpand = writable(false);
export const profileExpand = writable(false);
export const notificationExpand = writable(false);
export const navExpand = writable(true);
export const registrationExpand = writable(false);
export const selectExpand = writable(false);
export const selectProgramExpand = writable(false);
export const selectInstituteExpand = writable(false);
export const selectDeanInstituteExpand = writable(false);
export const dark = writable(false);
export const detailsExpand = writable(false);
export const sortExpand = writable(false);
export const actionExpand = writable(false);
