import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { Observable } from 'rxjs/Observable';

import { AuthService } from 'app/services/auth.service';

@Component({
  selector: 'volontulo-activation',
  templateUrl: './activation.component.html',
})
export class ActivationComponent implements OnInit {
  activationSuccessful: boolean;
  failureMessage: string;
  constructor(private authService: AuthService, private activatedRoute: ActivatedRoute
  ) {
  }

  activate(uuid: string): void {
    this.authService.activateAccount(uuid)
      .subscribe(
        rsp => {
          this.activationSuccessful = rsp.status === 201;
      },
        err => {

          this.activationSuccessful = false;
          if (err.status === 400) {
            this.failureMessage = 'Użytkownik został już aktywowany';
          } else if (err.status === 404) {
            this.failureMessage = 'Użytkownik nie istnieje';
          } else {
            this.failureMessage = 'Coś poszło nie tak, skontaktuj się z administratorem';
          }
      }
    );
  }

  ngOnInit() {
    this.activatedRoute.params.subscribe(params => {
      this.activate(params['token']);
    });
  }

}
