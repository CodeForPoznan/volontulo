export interface SuccessOrFailureAction {
  success: boolean;
  message?: string;
}

export interface FileReaderEventTarget extends EventTarget {
  result: string
}

export interface FileReaderEvent extends ProgressEvent {
  target: FileReaderEventTarget;
  getMessage(): string;
}
