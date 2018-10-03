import { HttpErrorResponse } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { inject, TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { environment } from '../environments/environment';
import { SuccessOrFailureAction } from './models';

import { AuthService } from './auth.service';
import { User } from './user';

describe('Auth service', () => {
  let service: AuthService;
  let httpTestingController: HttpTestingController;
  let subscribeExecuted: boolean;
  let router: Router;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ AuthService ],
      imports: [
        RouterTestingModule,
        HttpClientTestingModule,
      ],
    });
    httpTestingController = TestBed.get(HttpTestingController);
  });

  beforeEach(inject([AuthService, Router], (_authService, _router) => {
    router = _router;
    service = _authService;
  }));

  beforeEach(() => {
    httpTestingController.expectOne(`${environment.apiRoot}/current-user/`);
    subscribeExecuted = false;
  });

  afterEach(() => {
    httpTestingController.verify();
  });

  it('should inject service', () => {
    expect(service).toBeTruthy();
  });

  describe('getUser', () => {
    it('should make request to backend to get current user', () => {
      service.getUser()
        .subscribe(
          res => {
            subscribeExecuted = true;
            expect(res).toEqual({ email: 'cokolwiek'} as User)
          }
        );
    httpTestingController.expectOne(`${environment.apiRoot}/current-user/`).flush({email: 'cokolwiek'});
    expect(subscribeExecuted).toBe(true);
    });
  });

  describe('setCurrentUser', () => {
    it('should emit current user', () => {
      service.user$
      .subscribe(
        user => {
          subscribeExecuted = true;
          expect(user).toEqual({ email: 'cokolwiek' } as User);
        }
      );
    service.setCurrentUser({ email: 'cokolwiek'} as User);
    expect(subscribeExecuted).toBe(true);
    });
  });

  describe('login', () => {
    it('should login successfully and emit new current user', () => {
      let loginEventSubscriptionExecuted = false;
      service.user$
        .subscribe(
          user => {
            subscribeExecuted = true;
            expect(user).toEqual({ username: 'cokolwiek' } as User);
          }
        );
      service.login$.subscribe(
        (actionStatus: SuccessOrFailureAction) => {
          loginEventSubscriptionExecuted = true;
          expect(actionStatus).toEqual({ success: true });
        }
      );
      service.login('username@example', '123');
      httpTestingController.expectOne(`${environment.apiRoot}/login/`).flush({username: 'cokolwiek'} as User);
      expect(subscribeExecuted).toBe(true);
      expect(loginEventSubscriptionExecuted).toBe(true);
    });

    it('should emit error status when login failed', () => {
      spyOn(router, 'navigate');
      const mockErrorResponse = {
        status: 404,
        statusText: 'Bad Request'
      };
      service.login$
        .subscribe(
          (actionStatus: SuccessOrFailureAction) => {
            subscribeExecuted = true;
            expect((actionStatus as any).success).toBe(false);
          }
        );
      service.login('username@example', '123');
      httpTestingController.expectOne(`${environment.apiRoot}/login/`).flush('error' , mockErrorResponse);
      expect(router.navigate).not.toHaveBeenCalled();
      expect(subscribeExecuted).toBe(true);
    });
  });

  describe('resetPassword' , () => {
    it('should emit success when token to reset password was sent', () => {
      const mockSuccessResponse = {
        status: 201,
        statusText: 'CREATED'
      };
      service.resetPassword$
        .subscribe(
          (actionStatus: SuccessOrFailureAction) => {
            subscribeExecuted = true;
            expect(actionStatus.success).toBe(true);
          }
        );
      service.resetPassword('k@op.pl');
      httpTestingController.expectOne(`${environment.apiRoot}/password-reset/`).flush('Password changed', mockSuccessResponse );
      expect(subscribeExecuted).toBe(true);
    });

    it('should emit false when server returned status other than 201', () => {
      const mockSuccessResponse = {
        status: 200,
        statusText: 'OK'
      };
      service.resetPassword$
        .subscribe(
          (actionStatus: SuccessOrFailureAction) => {
            subscribeExecuted = true;
            expect(actionStatus.success).toBe(false);
            expect(actionStatus.message).toEqual('Backend return http code other than 201: 200');
          }
        );
      service.resetPassword('k@op.pl');
      httpTestingController.expectOne(`${environment.apiRoot}/password-reset/`)
        .flush('Token send', mockSuccessResponse );
      expect(subscribeExecuted).toBe(true);
    });

    it('should emit false with error when server returned error', () => {
      const mockErrorResponse = {
        status: 400,
        statusText: 'Bad request'
      };
      service.resetPassword$
        .subscribe(
          (actionStatus: SuccessOrFailureAction) => {
            subscribeExecuted = true;
            expect(actionStatus.success).toBe(false);
            expect(JSON.stringify(actionStatus.message)).toContain('Smth wen\'t wrong');
          }
        );
      service.resetPassword('k@op.pl');
      httpTestingController.expectOne(`${environment.apiRoot}/password-reset/`).flush('Smth wen\'t wrong', mockErrorResponse );
      expect(subscribeExecuted).toBe(true);
    });
  });

  describe('confirmResetPassword' , () => {
    it('should emit success when password was successfully reset', () => {
      const mockSuccessResponse = {
        status: 201, statusText: 'CREATED'
      };
      service.confirmResetPassword$
        .subscribe((actionStatus: SuccessOrFailureAction) => {
          subscribeExecuted = true;
          expect(actionStatus.success).toBe(true);
        });
      service.confirmResetPassword('111', '2222', '33333');
      httpTestingController.expectOne(`${environment.apiRoot}/password-reset/2222/33333/`)
        .flush('Password changed', mockSuccessResponse);
      expect(subscribeExecuted).toBe(true);
    });

    it('should emit status false when server returned status other than 201', () => {
      const mockSuccessResponse = {
        status: 200, statusText: 'OK'
      };
      service.confirmResetPassword$
        .subscribe((actionStatus: SuccessOrFailureAction) => {
          subscribeExecuted = true;
          expect(actionStatus.success).toBe(false);
          expect(actionStatus.message).toEqual('Backend return http code other than 201: 200');
        });
      service.confirmResetPassword('111', '2222', '33333');
      httpTestingController.expectOne(`${environment.apiRoot}/password-reset/2222/33333/`)
        .flush('I am lost', mockSuccessResponse);
      expect(subscribeExecuted).toBe(true);
    });

    it('should return false with error when server returned error', () => {
      const mockErrorResponse = {
        status: 400,
        statusText: 'Bad request'
      };
      service.confirmResetPassword$
        .subscribe(
          (actionStatus: SuccessOrFailureAction) => {
            subscribeExecuted = true;
            expect(actionStatus.success).toBe(false);
            expect(JSON.stringify(actionStatus.message)).toContain('Smth wen\'t wrong');
          }
        );
      service.confirmResetPassword('111', '2222', '33333');
      httpTestingController.expectOne(`${environment.apiRoot}/password-reset/2222/33333/`)
        .flush('Smth wen\'t wrong', mockErrorResponse);
      expect(subscribeExecuted).toBe(true);
    })
  });

  describe('register method', () => {
    it('should send request to server', () => {
      service.register('email@gmail.com', 'veryStrongPassword')
        .subscribe(
          response => expect(response.body).toEqual('Activation email was send')
        );
      httpTestingController.expectOne(`${environment.apiRoot}/register/`)
        .flush('Activation email was send');
    });
  });

  describe('activateAccount', () => {
    it('should send request to server', () => {
      service.activateAccount('123654')
        .subscribe(
          response => expect(response.body).toEqual('Welcome to the real world')
        );
      httpTestingController.expectOne(`${environment.apiRoot}/activate/123654/`)
        .flush('Welcome to the real world');
    });
  });

  describe('logout method', () => {
    it('should send request to the server, emit null as user and navigate to root path', () => {
      spyOn(router, 'navigate');
      service.user$
        .subscribe(
          user => {
            subscribeExecuted = true;
            expect(user).toBe(null);
          }
        );
      service.logout();
      httpTestingController.expectOne(`${environment.apiRoot}/logout/`)
        .flush(null);
      expect(router.navigate).toHaveBeenCalledWith(['/']);
      expect(subscribeExecuted).toBe(true);
    });
  });

  describe('update user', () => {
    it('should successfully update current user', () => {
      const testUser = {
        firstName: 'Jon',
        lastName: 'Doe',
        phoneNo: '444555666'
      };
      service.user$
      .subscribe(
        user => {
          subscribeExecuted = true;
          expect(user).toEqual(testUser as User);
      });
      service.updateUser(testUser as User);
      httpTestingController.expectOne(`${environment.apiRoot}/current-user/`)
        .flush(testUser);
      expect(subscribeExecuted).toBe(true);
    });
  });
});
