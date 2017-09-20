import { Component } from '@angular/core';

import { environment } from '../../environments/environment';
import { AuthService } from '../auth.service';
import { User } from '../user.d';

@Component({
  selector: 'volontulo-header',
  templateUrl: './header.component.html',
  providers: [AuthService]
})
export class HeaderComponent {

  private djangoRoot: string;
  private isNavbarCollapsed = true;
  private currentUser: User;

  constructor (private authService: AuthService) {
    this.djangoRoot = environment.djangoRoot;
    this.authService.changeUserEvent.subscribe(
      user => { this.currentUser = user; }
    );
  }

}
