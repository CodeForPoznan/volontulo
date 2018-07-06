import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { ReplaySubject } from 'rxjs/ReplaySubject';
import { Subject } from 'rxjs/Subject';
import { Observable } from 'rxjs/Observable';

import { User } from './user';
import { deepFreeze } from './utils/object.utils';
import { SuccessOrFailureAction } from './models';
import { environment } from '../environments/environment';

@Injectable()
export class AuthService {
  private currentUserUrl = `${environment.apiRoot}/current-user/`;
  private loginUrl = `${environment.apiRoot}/login/`;
  private logoutUrl = `${environment.apiRoot}/logout/`;
  private resetPasswordUrl = `${environment.apiRoot}/password-reset/`;
  private registerUrl = `${environment.apiRoot}/register/`;
  private activationUrl = `${environment.apiRoot}/activate/`;

  private changeUserEvent = new ReplaySubject<User | null>(1);
  private loginEvent = new Subject<SuccessOrFailureAction>();
  private resetPasswordEvent = new Subject<SuccessOrFailureAction>();
  private confirmResetPasswordEvent = new Subject<SuccessOrFailureAction>();
  private _currentUserUrl = `${environment.apiRoot}/current-user`;
  private _currentUser: User;

  public user$: Observable<User | null> = this.changeUserEvent.asObservable();
  public login$: Observable<SuccessOrFailureAction> = this.loginEvent.asObservable();
  public resetPassword$: Observable<SuccessOrFailureAction> = this.resetPasswordEvent.asObservable();
  public confirmResetPassword$: Observable<SuccessOrFailureAction> = this.confirmResetPasswordEvent.asObservable();

  constructor(
    private http: HttpClient,
    private router: Router,
  ) {
    this.getUser()
      .subscribe(
        user => {
          this.changeUserEvent.next(deepFreeze(user));
        },
        () => {
          this.changeUserEvent.next(null);
        },
      );
  }

  getUser(): Observable<User | null> {
    return this.http.get<User>(this.currentUserUrl);
  }

  setCurrentUser(user: User) {
    this.changeUserEvent.next(deepFreeze(user));
  }

  login(username: string, password: string): void {
    this.http.post<User>(this.loginUrl, { username, password })
      .subscribe(
        user => {
          this.changeUserEvent.next(deepFreeze(user));
          this.loginEvent.next({ success: true });
          this.router.navigate(['']);
        },
        err => {
          this.loginEvent.next({ success: false, message: err });
        }
      );
  }

  resetPassword(username: string) {
    this.http.post(
      this.resetPasswordUrl, { username }, { observe: 'response' })
      .subscribe(
        response => {
          if (response.status === 201) {
            this.resetPasswordEvent.next({ success: true });
          } else {
            this.resetPasswordEvent.next(
              {
                success: false,
                message: `Backend return http code other than 201: ${response.status}`
              });
          }
        },
        err => {
          this.resetPasswordEvent.next({ success: false, message: err });
        });
  }

  confirmResetPassword(password: string, uidb64: string, token: string) {
    this.http.post(
      `${this.resetPasswordUrl}${uidb64}/${token}/`, { password }, { observe: 'response' })
      .subscribe(
        response => {
          if (response.status === 201) {
            this.confirmResetPasswordEvent.next({ success: true });
          } else {
            this.confirmResetPasswordEvent.next(
              {
                success: false,
                message: `Backend return http code other than 201: ${response.status}`
              });
          }
        },
        err => {
          this.confirmResetPasswordEvent.next({ success: false, message: err });
        });
  }

  register(email: string, password: string) {
    return this.http.post(
      this.registerUrl,
      { password, email },
      { observe: 'response' })
  }

  activateAccount(uuid: string) {
    return this.http.post(
      `${this.activationUrl}${uuid}/`,
      null,
      { observe: 'response' });
  }

  logout() {
    this.http.post(this.logoutUrl, {})
      .subscribe(_ => {
        this.changeUserEvent.next(null);
        this.router.navigate(['/']);
      });
  }

  updateUser(data: Partial<User>) {
    this.http.post<User>(`${environment.apiRoot}/current-user/`, data)
      .subscribe(user => this.changeUserEvent.next(user));
  }
}
