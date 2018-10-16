import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { faMapMarkerAlt, faClock, faEdit } from '@fortawesome/free-solid-svg-icons';
import { Observable } from 'rxjs/Observable';
import { combineLatest } from 'rxjs/operators/combineLatest';
import 'rxjs/add/operator/switchMap';

import { Offer } from 'app/models/offer.model';
import { User } from 'app/models/user.model';
import { AuthService } from 'app/services/auth.service';
import { OffersService } from 'app/services/offers.service';
import { environment } from 'environments/environment';

@Component({
  selector: 'volontulo-offer-detail',
  templateUrl: './offer-detail.component.html',
  styleUrls: ['./offer-detail.component.scss'],
})
export class OfferDetailComponent implements OnInit {
  public offer$: Observable<Offer>;
  public getJoinViewUrl = this.offersService.getJoinViewUrl;
  isUserOrgMember$: Observable<boolean>;
  user$: Observable<User | null>;
  faMapMarkerAlt = faMapMarkerAlt;
  faClock = faClock;
  faEdit = faEdit;

  constructor(
    private activatedRoute: ActivatedRoute,
    private authService: AuthService,
    private offersService: OffersService,
  ) { }

  ngOnInit() {
    this.user$ = this.authService.user$;
    this.offer$ = this.activatedRoute.params
      .switchMap(params => this.offersService.getOffer(params.offerId))

    this.isUserOrgMember$ = this.offer$
      .pipe(combineLatest(this.user$, (offer, user): boolean => {
        if (offer && user) {
          const filteredOrganizations = user.organizations.filter(organ => organ.id === offer.organization.id);
          return filteredOrganizations.length > 0;
        }
        return false;
      }));
    }
}
