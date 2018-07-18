import { Component, ViewChild } from '@angular/core';
import { RegisterRequestModel } from 'app/auth.models';
import { AuthService } from '../auth.service';
import { Observable } from 'rxjs/Observable';
import { RedirectComponent } from 'app/redirect.component';
import { Params } from '@angular/router';
import { NgControl } from '@angular/forms';

@Component({
  selector: 'volontulo-register',
  templateUrl: './register.component.html',
})
export class RegisterComponent {
  registerModel: RegisterRequestModel = {
    email: '',
    password: '',
  };
  honeyBunny = '';
  ACCEPT_TERMS = 'Wyrażam zgodę na przetwarzanie moich danych osobowych';
  registrationSuccessful = false;
  userIsAuthenticated = false;

  @ViewChild('checkboxTA') public checkboxTA: NgControl;

  constructor(private authService: AuthService,
  ) {
  }

  register(): void {
    if (this.honeyBunny === '') {
      this.checkboxTA.control.markAsDirty();
      if (!this.checkboxTA.control.value) {
        return;
      }

      this.registrationSuccessful = false;
      this.userIsAuthenticated = false;
      this.authService.register(this.registerModel.email, this.registerModel.password)
        .subscribe(rsp => {
          if (rsp.status === 201) {
            this.registrationSuccessful = true;
        }
        );
    }
  }
}
