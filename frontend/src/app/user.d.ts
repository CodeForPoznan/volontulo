import { Organization } from './organization/organization.model';

export interface User {
  is_administrator: boolean,
  organizations: Array<Organization>,
  username: string,
}
