import { Component } from '@angular/core';

import { AuthService } from '../auth.service';
import { User } from '../user.d';
import { Observable } from 'rxjs/Observable';

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
