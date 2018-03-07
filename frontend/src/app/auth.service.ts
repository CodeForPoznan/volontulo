import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';

import { environment } from '../environments/environment';
import { User } from './user.d';
import { SuccessOrFailureAction } from './models';


@Injectable()
export class AuthService {
  private currentUserUrl = `${environment.apiRoot}/current-user`;
  private loginUrl = `${environment.apiRoot}/login`;
  private logoutUrl = `${environment.apiRoot}/logout`;
  private resetPasswordUrl = `${environment.apiRoot}/password-reset`;

  private changeUserEvent = new BehaviorSubject<User | null>(null);
  private loginEvent = new BehaviorSubject<SuccessOrFailureAction | null>(null);
  private logoutEvent = new BehaviorSubject<SuccessOrFailureAction | null>(null);
  private resetPasswordEvent = new BehaviorSubject<SuccessOrFailureAction | null>(null);
  private confirmResetPasswordEvent = new BehaviorSubject<SuccessOrFailureAction | null>(null);

  public user$: Observable<User | null> = this.changeUserEvent.asObservable();
  public login$: Observable<SuccessOrFailureAction | null> = this.loginEvent.asObservable();
  public logout$: Observable<SuccessOrFailureAction | null> = this.logoutEvent.asObservable();
  public resetPassword$: Observable<SuccessOrFailureAction | null> = this.resetPasswordEvent.asObservable();
  public confirmResetPassword$: Observable<SuccessOrFailureAction | null> = this.confirmResetPasswordEvent.asObservable();

  constructor(
    private http: HttpClient,
    private router: Router,
  ) {
    this.http.get<User>(this.currentUserUrl)
      .subscribe(user => {
        if (user.username) {
          this.changeUserEvent.next(user);
        } else {
          this.changeUserEvent.next(null);
        }
      });
  }

  login(username: string, password: string): void {
    this.http.post<User>(this.loginUrl, { username, password })
      .subscribe(
        user => {
          this.changeUserEvent.next(user);
          this.loginEvent.next({ result: 'success'});
          this.router.navigate(['']);
        },
        err => {
          this.loginEvent.next({ result: 'failure', message: err });
        }
      );
  }

  resetPassword(username: string) {
    this.http.post(
      this.resetPasswordUrl, { username }, { observe: 'response' })
      .subscribe(
        response => {
          if (response.status === 201) {
            this.resetPasswordEvent.next({ result: 'success' });
          } else {
            this.resetPasswordEvent.next(
              {
                result: 'failure',
                message: `Backend return http code other than 201: ${ response.status }`
              });
          }
        },
        err => {
          this.resetPasswordEvent.next({ result: 'failure', message: err });
        });
  }

  confirmResetPassword(password: string, uidb64: string, token: string) {
    this.http.post(
      `${this.resetPasswordUrl}/${uidb64}/${token}`, { password }, { observe: 'response' })
      .subscribe(
        response => {
          if (response.status === 201) {
            this.confirmResetPasswordEvent.next({ result: 'success' });
          } else {
            this.confirmResetPasswordEvent.next(
              {
                result: 'failure',
                message: `Backend return http code other than 201: ${ response.status }`
              });
          }
        },
        err => {
          this.confirmResetPasswordEvent.next({ result: 'failure', message: err });
        });
  }

  logout() {
    this.http.post<any>(this.logoutUrl, {})
      .subscribe(_ => {
        this.changeUserEvent.next(null);
        this.router.navigate(['/']);
      });
  }
}
