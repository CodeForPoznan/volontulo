import { HttpClient } from '@angular/common/http';
import { Component, Inject } from '@angular/core';
import { Observable } from 'rxjs/Observable';

import { environment } from '../../environments/environment';
import { WindowService } from '../window.service';

interface Message {
  message: string;
  showMessage: boolean;
  type: string;
}

@Component({
  selector: 'volontulo-messages',
  templateUrl: './messages.component.html',
})
export class MessagesComponent {
  messages$: Observable<Message[]>;
  showMessages = true;

  constructor(
    private http: HttpClient,
        @Inject(WindowService) private window: any) {
    this.messages$ = this.http.get<Message[]>(
      `${environment.apiRoot}/messages/`).map(response => {
      window.setTimeout(() => this.showMessages = false, 25000);
      return response.map(message => {
        message.showMessage = true;
        return message;
      });
    });
   }

   closeMessage(message: Message): void {
     message.showMessage = false;
   }
}
