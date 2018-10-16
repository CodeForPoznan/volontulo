export interface Organization {
  address: string;
  description: string;
  id: number;
  slug: string;
  name: string;
  url: string;
}

export interface OrganizationContactPayload {
  name: string;
  email: string;
  phone_no: string;
  message: string;
}

export interface ContactStatus {
  data: any;
  status: 'success' | 'error';
}

export interface CreateOrEditOrganization {
  data: any;
  type: 'create' | 'edit' | 'error';
}
