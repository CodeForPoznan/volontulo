import { Organization } from 'app/models/organization.model';

export interface User {
  email: string,
  firstName: string,
  isAdministrator: boolean,
  lastName: string,
  organizations: Array<Organization>,
  phoneNo: string;
  username: string,
}
