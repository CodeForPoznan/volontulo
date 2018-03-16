import { Organization } from './organization/organization.model';

export interface User {
  isAdministrator: boolean,
  organizations: Array<Organization>,
  username: string,
}
