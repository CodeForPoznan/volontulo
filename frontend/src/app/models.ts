export interface Action {
  result: any;
}

export interface SuccessOrFailureAction extends Action {
  result: 'success' | 'failure'
  message?: string;
}
