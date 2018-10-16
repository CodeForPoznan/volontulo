import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { filter, skip } from 'rxjs/operators';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/of';

import { LoginRequestModel } from 'app/models/auth.models';
import { AuthService } from 'app/services/auth.service';

@Component({
  selector: 'volontulo-login',
  templateUrl: './login.component.html',
})
export class LoginComponent implements OnInit {
  loginModel: LoginRequestModel = {
    username: '',
    password: '',
  };
  loginError$: Observable<any>;

  constructor(private authService: AuthService) { }

  ngOnInit() {
    this.loginError$ = this.authService.login$.pipe(
      filter(action => !action.success),
    );
  }

  login(): void {
    this.authService.login(this.loginModel.username, this.loginModel.password);
  }
}
