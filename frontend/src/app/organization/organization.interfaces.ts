export interface ContactStatus {
  data: any;
  status: 'success' | 'error';
}

export interface CreateOrEditOrganization {
  data: any;
  type: 'create' | 'edit' | 'error';
}
