import { EventEmitter, Injectable } from '@angular/core';
import { Http } from '@angular/http';

import { environment } from '../environments/environment';
import { User } from './user.d';
import { Router } from '@angular/router';

@Injectable()
export class AuthService {
  private _loginUrl = `${environment.apiRoot}/login`;
  private _logoutUrl = `${environment.apiRoot}/logout`;
  private _currentUserUrl = `${environment.apiRoot}/current-user`;
  private _currentUser: User;
  public changeUserEvent: EventEmitter<User>;
  public resetPasswordUrl = `${environment.djangoRoot}/password-reset`;

  constructor(
    private http: Http,
    private router: Router,
  ) {
    this.changeUserEvent = new EventEmitter<User>();

    this.http.get(this._currentUserUrl, { withCredentials: true })
      .subscribe(rsp => {
        this._currentUser = (rsp.text() === '' ? null : rsp.json());
        this.changeUserEvent.emit(this._currentUser);
      });
  }

  login(username: string, password: string) {
    this.http.post(
      this._loginUrl,
      { username, password },
      { withCredentials: true })
      .subscribe(rsp => {
        const backendUser = rsp.json();
        if (this._currentUser !== backendUser) {
          this._currentUser = backendUser;
          this.changeUserEvent.emit(this._currentUser);
          this.router.navigate(['']);
        }
      });
  }

  currentUser(): User {
    return this._currentUser;
  }

}
