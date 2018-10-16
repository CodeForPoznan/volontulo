import { Component, OnInit, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { filter, skip } from 'rxjs/operators';

import { AuthService } from 'app/services/auth.service';

@Component({
  selector: 'volontulo-password-reset',
  templateUrl: './password-reset.component.html',
  styleUrls: ['./password-reset.component.scss'],
})
export class PasswordResetComponent implements OnInit {
  @ViewChild('resetForm') resetForm: NgForm;
  alertSuccessVisible = false;

  constructor(private authService: AuthService) { }

  public ngOnInit() {
    this.authService.resetPassword$.pipe(
      filter(action => action.success),
    ).subscribe(action => {
      this.alertSuccessVisible = true;
      this.resetForm.reset();
    });
  }

  onSubmit(): void {
    this.authService.resetPassword(this.resetForm.value.username);
  }

  hideSuccessAlert() {
    this.alertSuccessVisible = false;
  }
}
