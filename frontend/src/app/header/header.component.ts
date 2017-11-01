import { Component } from '@angular/core';

import { environment } from '../../environments/environment';
import { AuthService } from '../auth.service';
import { User } from '../user.d';

@Component({
  selector: 'volontulo-header',
  templateUrl: './header.component.html',
})
export class HeaderComponent {

  public currentUser: User;
  public djangoRoot: string;
  public isNavbarCollapsed = true;

  constructor (private authService: AuthService) {
    this.djangoRoot = environment.djangoRoot;
    this.authService.changeUserEvent.subscribe(
      user => { this.currentUser = user; }
    );
  }

}
