import { Component } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/of';

import { LoginRequestModel } from '../auth.models';
import { AuthService } from '../auth.service';

@Component({
  selector: 'volontulo-login',
  templateUrl: './login.component.html',
})
export class LoginComponent {
  loginModel: LoginRequestModel = {
    username: '',
    password: '',
  };
  isAuthFailed: boolean;
  resetPasswordUrl = this.authService.resetPasswordUrl;

  constructor(private authService: AuthService,
  ) { }

  login(): void {
    this.authService.login(this.loginModel.username, this.loginModel.password)
      .catch(error => {
        if (error.status === 401) {
          this.isAuthFailed = true;
        }
        return Observable.of(null);
      })
      .subscribe();
  }

}
