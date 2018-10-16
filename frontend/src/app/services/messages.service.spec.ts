import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { fakeAsync, tick, TestBed, inject } from '@angular/core/testing';
import { Observable } from 'rxjs/Observable';
import { ISubscription } from 'rxjs/Subscription';

import {
  MessagesService,
  Message,
  MessageType,
  DEFAULT_TIMEOUT_TIME,
  ServerMessage
} from 'app/services/messages.service';
import { environment } from 'environments/environment';

describe('MessagesService', () => {
  let service: MessagesService;
  let httpMock: HttpTestingController;
  let testMessage: Message;
  let messageSubscription: ISubscription;

  this.subscribeToMessage$ = (assertionCallback: (Message) => void) => {
    messageSubscription = service.message$.subscribe(assertionCallback)
  }

  this.assertMessageEquals = (msg, testMsg) => {
    expect(msg).toEqual(testMsg)
  }

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [MessagesService]
    });

    service = TestBed.get(MessagesService);
    httpMock = TestBed.get(HttpTestingController);
    testMessage = {
      message: 'Test message',
      type: MessageType.Info,
      dismissible: true,
      timeout: DEFAULT_TIMEOUT_TIME
    }
    spyOn(this, 'assertMessageEquals').and.callThrough();
  });

  afterEach(() => {
    httpMock.verify();
    service = null;
    testMessage = null;

    if (messageSubscription) {
      messageSubscription.unsubscribe();
      messageSubscription = null;
    }
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('Messages are correctly exposed through observable', () => {
    it('showMessage() should send generic message', fakeAsync(() => {
      this.subscribeToMessage$(msg => this.assertMessageEquals(msg, testMessage));
      // Method called with one parameter
      service.showMessage(testMessage.message);

      // Method called with multiple parameters
      testMessage.type = MessageType.Danger;
      testMessage.dismissible = false;
      testMessage.timeout = 5;
      service.showMessage(testMessage.message, MessageType.Danger, false, 5);

      expect(this.assertMessageEquals).toHaveBeenCalledTimes(2);
    }));

    it('success() should send message type success', fakeAsync(() => {
      this.subscribeToMessage$(msg => this.assertMessageEquals(msg, testMessage));
      // Method called with one parameter
      testMessage.type = MessageType.Success;
      service.success(testMessage.message);

      // Method called with multiple parameters
      testMessage.dismissible = false;
      testMessage.timeout = 5;
      service.success(testMessage.message, false, 5);

      expect(this.assertMessageEquals).toHaveBeenCalledTimes(2);
    }));

    it('info() should send message type info', fakeAsync(() => {
      this.subscribeToMessage$(msg => this.assertMessageEquals(msg, testMessage));
      // Method called with one parameter
      service.info(testMessage.message);

      // Method called with multiple parameters
      testMessage.dismissible = false;
      testMessage.timeout = 5;
      service.info(testMessage.message, false, 5);

      expect(this.assertMessageEquals).toHaveBeenCalledTimes(2);
    }));

    it('warning() should send message type warning', fakeAsync(() => {
      this.subscribeToMessage$(msg => this.assertMessageEquals(msg, testMessage));
      // Method called with one parameter
      testMessage.type = MessageType.Warning;
      service.warning(testMessage.message);

      // Method called with multiple parameters
      testMessage.dismissible = false;
      testMessage.timeout = 5;
      service.warning(testMessage.message, false, 5);

      expect(this.assertMessageEquals).toHaveBeenCalledTimes(2);
    }));

    it('danger() should send message type danger', () => {
      this.subscribeToMessage$(msg => this.assertMessageEquals(msg, testMessage));
      // Method called with one parameter
      testMessage.type = MessageType.Danger;
      service.danger(testMessage.message);

      // Method called with multiple parameters
      testMessage.dismissible = false;
      testMessage.timeout = 5;
      service.danger(testMessage.message, false, 5);

      expect(this.assertMessageEquals).toHaveBeenCalledTimes(2);
    });

    it('clear() should send null value', fakeAsync(() => {
      testMessage = null;
      this.subscribeToMessage$(msg => this.assertMessageEquals(msg, testMessage));
      service.clear();

      expect(this.assertMessageEquals).toHaveBeenCalledTimes(1);
    }));

    it('fetchServerMessages() correctly returns messages from backend', fakeAsync(() => {
      /* Arrange */
      spyOn(service, 'showMessage').and.callThrough();
      const serverMessages: Array<ServerMessage> = [
        { message: 'Server Message Debug', type: 'debug' },
        { message: 'Server Message Info', type: 'info' },
        { message: 'Server Message Success', type: 'success' },
        { message: 'Server Message Warning', type: 'warning' },
        { message: 'Server Message Error', type: 'error' }
      ];

      let numberOfCalls = 0;
      service.message$.subscribe(msg => {
        const serverMsg: ServerMessage = serverMessages[numberOfCalls];
        const expectedMessage: Message = {
          message: serverMsg.message,
          type: serverMsg.type,
          dismissible: true,
          timeout: 1.5 * DEFAULT_TIMEOUT_TIME
        }

        // Change message type when there is no match with Django message type
        if (numberOfCalls === 0) {
          expectedMessage.type = MessageType.Info;
        } else if (numberOfCalls === 4) {
          expectedMessage.type = MessageType.Danger;
        }

        expect(msg).toEqual(expectedMessage)
        numberOfCalls++;
      })

      /* Act */
      service.fetchServerMessages();

      /* Assert */
      const req = httpMock.expectOne(`${environment.apiRoot}/messages/`);
      expect(req.request.method).toBe('GET');
      req.flush(serverMessages);

      expect(service.showMessage).toHaveBeenCalledTimes(5);
    }));
  });
});
