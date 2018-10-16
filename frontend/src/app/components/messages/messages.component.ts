import { Component, Inject, OnInit, OnDestroy } from '@angular/core';
import { ISubscription } from 'rxjs/Subscription';

import { MessagesService, Message } from 'app/services/messages.service';
import { WindowService } from 'app/services/window.service';

@Component({
  selector: 'volontulo-messages',
  templateUrl: './messages.component.html'
})
export class MessagesComponent implements OnInit, OnDestroy {
  private messageSubscription: ISubscription;
  public messages: Message[] = [];

  constructor(private messagesService: MessagesService,
    @Inject(WindowService) private window: any) { }

  ngOnInit() {
    this.messageSubscription = this.messagesService.message$
      .subscribe((message: Message) => {
        if (!message) {
          this.messages = [];
          return;
        }

        this.addMessageTimeout(message);
        this.messages.push(message);
      });
    this.messagesService.fetchServerMessages();
  }

  private addMessageTimeout(message) {
    if (message.timeout > 0) {
      this.window.setTimeout(
        () => this.closeMessage(message), message.timeout * 1000);
    }
  }

  closeMessage(message: Message) {
    // Closes the message by filtering it out of messages[]
    this.messages = this.messages.filter(msg => msg !== message);
  }

  ngOnDestroy() {
    this.messageSubscription.unsubscribe();
  }
}
