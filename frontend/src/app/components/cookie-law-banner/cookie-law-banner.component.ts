import { Component } from '@angular/core';
import { CookieService } from 'ngx-cookie';

@Component({
  selector: 'volontulo-cookie-law-banner',
  templateUrl: './cookie-law-banner.component.html',
  styleUrls: ['./cookie-law-banner.component.scss']
})
export class CookieLawBannerComponent {
  public shouldHide: boolean;

  constructor(private _cookieService: CookieService) {
    this.shouldHide = (!!this._cookieService.get('cookielaw_accepted'));
  }

  acceptCookieLaw() {
    const tenYearsFromNow = new Date().setFullYear(new Date().getFullYear() + 10);
    this._cookieService.put('cookielaw_accepted', '1', {
      expires: new Date(tenYearsFromNow)
    });
    this.shouldHide = true;
  }

}
