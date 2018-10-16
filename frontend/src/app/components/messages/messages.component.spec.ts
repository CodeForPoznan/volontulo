import { PLATFORM_ID } from '@angular/core';
import { async, fakeAsync, tick, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { Subject } from 'rxjs/Subject';

import { MessagesComponent } from 'app/components/messages/messages.component';
import { MessagesService, Message, MessageType } from 'app/services/messages.service';
import { WindowFactory, WindowService } from 'app/services/window.service';


describe('MessagesComponent', () => {
  let component: MessagesComponent;
  let fixture: ComponentFixture<MessagesComponent>;
  let service: MessagesService;

  const messageSubject = new Subject<Message>();
  const testMessages: Message[] = [
    {
      message: 'Test server message 1',
      type: MessageType.Success,
      dismissible: true,
      timeout: 0.8
    },
    {
      message: 'Test message 1',
      type: MessageType.Success,
      dismissible: true,
      timeout: 0
    }, {
      message: 'Test message 2',
      type: MessageType.Info,
      dismissible: false,
      timeout: 0.8
    }, {
      message: 'Test message 3',
      type: MessageType.Danger,
      dismissible: true,
      timeout: 0.95
    }
  ];

  const messagesServiceStub = {
    message$: messageSubject.asObservable(),
    fetchServerMessages: () => {
      messageSubject.next(testMessages[0]);
    }
  }

  this.initTestMessages = () => {
    for (const message of testMessages.slice(1)) {
      messageSubject.next(message);
    }
  }

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        NgbModule.forRoot()
      ],
      providers: [
        { provide: MessagesService, useValue: messagesServiceStub },
        {
          provide: WindowService, useFactory: WindowFactory,
          deps: [PLATFORM_ID]
        }
      ],
      declarations: [MessagesComponent]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MessagesComponent);
    component = fixture.componentInstance;
    service = TestBed.get(MessagesService);
    spyOn(service, 'fetchServerMessages').and.callThrough();
  });

  afterEach(() => {
    fixture.destroy();
    component = null;
    service = null;
  })

  describe('Synchronous MessagesComponent tests', () => {
    beforeEach(() => {
      fixture.detectChanges();
    });

    it('should create', () => {
      expect(component).toBeTruthy();
    });

    it('should show server messages after init', () => {
      expect(service.fetchServerMessages).toHaveBeenCalledTimes(1);
      expect(component.messages.length).toEqual(1);

      const alertContainer = fixture.nativeElement.querySelector('.alert');
      expect(alertContainer).toBeTruthy();

      const textContainer = alertContainer.querySelector('div');
      expect(textContainer.textContent).toEqual(testMessages[0].message);
    });

    it('should render incoming messages properly', () => {
      // After ngOnInit, fetchServerMessages returns a message, hence we expect 1
      expect(component.messages.length).toEqual(1);
      this.initTestMessages();
      expect(component.messages.length).toEqual(4);
      fixture.detectChanges();

      const alerts = fixture.debugElement.queryAll(By.css('.alert'));
      expect(alerts.length).toEqual(4);

      alerts.forEach((alertEl, idx) => {
        const textContainer = alertEl.nativeElement.querySelector('div');
        expect(textContainer.textContent).toEqual(testMessages[idx].message);
      });
    });

    it('should close the message after click on dismiss', () => {
      spyOn(component, 'closeMessage').and.callThrough();
      expect(component.messages.length).toEqual(1);

      const dismissButton = fixture.debugElement
        .query(By.css('.alert-dismissible button'));
      dismissButton.triggerEventHandler('click', null);

      expect(component.closeMessage).toHaveBeenCalled();
      expect(component.messages.length).toEqual(0);
    });

    it('should delete messages when null observable value is received', () => {
      this.initTestMessages();
      expect(component.messages.length).toEqual(4);
      messageSubject.next();
      expect(component.messages.length).toEqual(0);
    })
  });

  it('should close and delete messages after timeout time', fakeAsync(() => {
    spyOn(component, 'closeMessage').and.callThrough();
    fixture.detectChanges();
    this.initTestMessages();
    expect(component.messages.length).toEqual(4);

    // We tick for 1000ms as max timeout for messages in this test is set to 950ms.
    tick(1000);

    expect(component.closeMessage).toHaveBeenCalledTimes(3);
    expect(component.messages.length).toEqual(1);
  }));
});
