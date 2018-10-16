import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';

import { environment } from 'environments/environment';

export interface ServerMessage {
  message: string;
  type: string;
}

export class Message {
  message: string;
  type: string;
  dismissible: boolean;
  /** Timeout is set in seconds, not ms. Can be floating-point. */
  timeout?: number;
}

export enum MessageType {
  Success = 'success',
  Info = 'info',
  Warning = 'warning',
  Danger = 'danger',
  Primary = 'primary',
  Secondary = 'secondary',
  Light = 'light',
  Dark = 'dark'
}

export const DEFAULT_TIMEOUT_TIME = 7.5;

@Injectable()
export class MessagesService {
  private messageSubject = new Subject<Message>();
  public message$ = this.messageSubject.asObservable();

  constructor(private http: HttpClient) { }

  private nextMessage(message?: Message) {
    this.messageSubject.next(message);
  }

  showMessage(message: string, type = MessageType.Info, dismissible = true,
    timeout = DEFAULT_TIMEOUT_TIME) {
    this.nextMessage({ message, type, dismissible, timeout });
  }

  success(message: string, dismissible = true, timeout = DEFAULT_TIMEOUT_TIME) {
    this.showMessage(message, MessageType.Success, dismissible, timeout);
  }

  info(message: string, dismissible = true, timeout = DEFAULT_TIMEOUT_TIME) {
    this.showMessage(message, MessageType.Info, dismissible, timeout);
  }

  warning(message: string, dismissible = true, timeout = DEFAULT_TIMEOUT_TIME) {
    this.showMessage(message, MessageType.Warning, dismissible, timeout);
  }

  danger(message: string, dismissible = true, timeout = DEFAULT_TIMEOUT_TIME) {
    this.showMessage(message, MessageType.Danger, dismissible, timeout);
  }

  fetchServerMessages() {
    this.http.get<ServerMessage[]>(`${environment.apiRoot}/messages/`)
      .subscribe(serverMessages => {
        serverMessages
          .forEach(serverMsg => {
            const type = this.getFrontendMessageType(serverMsg.type);
            // Reasoning for multiplying default timeout time: we do not get
            // control of how long is the message received from the server and how many
            // of them are received at the same time. If they stack on each other,
            // default timeout time will be to short to read them all, whereas
            // it is usually enough to read just one, even longer, message.
            this.showMessage(serverMsg.message, type, true, 1.5 * DEFAULT_TIMEOUT_TIME);
          });
      });
  }

  private getFrontendMessageType(type: string): MessageType {
    if (Object.values(MessageType).includes(type)) {
      return type as MessageType;
    } else if (type === 'error') {
      return MessageType.Danger;
    } else {
      return MessageType.Info;
    }
  }

  clear() {
    this.nextMessage(null);
  }
}
