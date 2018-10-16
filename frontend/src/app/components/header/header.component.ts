import { Component } from '@angular/core';
import { Observable } from 'rxjs/Observable';

import { User } from 'app/models/user.model';
import { AuthService } from 'app/services/auth.service';

@Component({
  selector: 'volontulo-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent {

  public currentUser$: Observable<User | null>;
  public isNavbarCollapsed = true;

  constructor (private authService: AuthService) {
    this.currentUser$ = this.authService.user$;
  }

  public logout() {
    this.authService.logout();
  }
}
