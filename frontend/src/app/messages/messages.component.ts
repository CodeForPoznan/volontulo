import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Observable } from 'rxjs/Observable';

import { environment } from '../../environments/environment';

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

  constructor(private http: HttpClient) {
    this.messages$ = this.http.get<Message[]>(
      `${environment.apiRoot}/messages/`).map(response => {
      setTimeout(() => this.showMessages = false, 25000);
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
