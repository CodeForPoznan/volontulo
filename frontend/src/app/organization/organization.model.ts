export interface Organization {
  address: string;
  description: string;
  id: number;
  slug: string;
  name: string;
}

export interface OrganizationContactPayload {
  name: string;
  email: string;
  phone_no: string;
  message: string;
}
