import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { User } from '../user';
import { AuthService } from '../auth.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { skip, take } from 'rxjs/operators';

@Component({
  selector: 'volontulo-user-profile',
  templateUrl: './user-profile.component.html',
})
export class UserProfileComponent implements OnInit {
  public user$: Observable<User>;

  public fg: FormGroup = this.fb.group({
    first_name: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(30)]],
    last_name: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(30)]],
    phone_no: ['', [Validators.maxLength(32)]],
  });
  public submitEnabled = true;
  public success: null | boolean = null;

  constructor(
    private authService: AuthService,
    private fb: FormBuilder,
  ) { }

  ngOnInit() {
    this.user$ = this.authService.user$;

    this.user$.subscribe(user => {
      this.fg.controls.first_name.setValue(user.firstName);
      this.fg.controls.last_name.setValue(user.lastName);
      this.fg.controls.phone_no.setValue(user.phoneNo);
    });
  }

  updateUser() {
    if (this.fg.valid) {
      this.user$.pipe(
        skip(1),
        take(1),
      ).subscribe(
        () => this.success = true,
        () => this.success = false,
      );
      this.authService.updateUser(this.fg.value);
    }
  }
}
