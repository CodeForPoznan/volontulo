import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { map, take } from 'rxjs/operators';

import { Organization } from 'app/models/organization.model';
import { User } from 'app/models/user.model';
import { AuthService } from 'app/services/auth.service';

@Injectable()
export class UserService {

  constructor (private authService: AuthService) {}

  addOrganization(organization: Organization): Observable<User> {
    return this.authService.user$.pipe(
      take(1),
      map(user => {
        const alteredUser = {
          ...user,
          organizations: [...user.organizations, organization],
        };
        this.authService.setCurrentUser(alteredUser);
        return alteredUser;
      })
    );
  }
  updateOrganization(organization: Organization) {
    return this.authService.user$.pipe(
      take(1),
      map(user => {
        const index = user.organizations.findIndex(org => org.id === organization.id);
        const alteredUser = {
          ...user,
          organizations: [
            ...user.organizations.slice(0, index - 1),
            organization,
            ...user.organizations.slice(index + 1)
          ],
        };
        this.authService.setCurrentUser(alteredUser);
        return alteredUser;
      })
    );
  }

  getFullName(user: User): string {
    return `${user.firstName} ${user.lastName}`;
  }
}
