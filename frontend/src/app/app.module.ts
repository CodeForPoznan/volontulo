import { ErrorHandler, NgModule } from '@angular/core';
import { OffersService } from './homepage-offer/offers.service';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule, Routes } from '@angular/router';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CookieModule } from 'ngx-cookie';
import * as Raven from 'raven-js';

import { environment } from '../environments/environment';
import { AppComponent } from './app.component';
import { RedirectComponent } from './redirect.component';
import { WindowService, WindowFactory } from './window.service';
import { OrganizationService } from './organization/organization.service';
import { OrganizationDetailsComponent } from './organization/organization-details/organization-details.component';
import { HomepageOfferComponent } from './homepage-offer/homepage-offer.component';
import { HomePageComponent } from './home/homepage.component';
import { FooterComponent } from './footer/footer.component';
import { HeaderComponent } from './header/header.component';
import { CookieLawBannerComponent } from './cookie-law-banner/cookie-law-banner.component';
import { AboutUsComponent } from './static/about-us.component';
import { RegulationsComponent } from './static/regulations.component';
import { LoginComponent } from './login/login.component';
import { AuthService } from './auth.service';
import { OfferDetailComponent } from './offers/offer-detail/offer-detail.component';
import { IconComponent } from './icon/icon.component';
import { IconLabelComponent } from './icon-label/icon-label.component';
import { BannerComponent } from './banner/banner.component';
import { FaqOrganizationsComponent } from './static/faq-organizations.component';
import { OrganizationContactComponent } from './organization/organization-contact/organization-contact.component';
import { OrganizationComponent } from './organization/organization.component';
import { OfficeComponent } from './static/office/office.component';
import { FaqVolunteersComponent } from './static/faq-volunteers.component';

Raven.config(environment.sentryDSN).install();

export class RavenErrorHandler implements ErrorHandler {
  handleError(err: any): void {
    Raven.captureException(err);
  }
}

const appRoutes: Routes = [
  {
    path: '',
    component: HomePageComponent
  },
  {
    path: 'organizations/:organizationSlug/:organizationId',
    component: OrganizationComponent,
  },
  {
    path: 'faq-organizations',
    component: FaqOrganizationsComponent,
  },
  {
    path: 'faq-volunteers',
    component: FaqVolunteersComponent,
  },
  {
    path: 'office',
    component: OfficeComponent,
  },
  {
    path: 'about-us',
    component: AboutUsComponent
  },
  {
    path: 'login',
    component: LoginComponent,
  },
  {
    path: 'regulations',
    component: RegulationsComponent
  },
  {
    path: 'offers/:offerSlug/:offerId',
    component: OfferDetailComponent,
  },
  {
    path: '**',
    component: RedirectComponent
  }
];

@NgModule({
  declarations: [
    AppComponent,
    RedirectComponent,
    HomePageComponent,
    HeaderComponent,
    FooterComponent,
    OrganizationDetailsComponent,
    HomepageOfferComponent,
    CookieLawBannerComponent,
    AboutUsComponent,
    RegulationsComponent,
    LoginComponent,
    OfferDetailComponent,
    IconComponent,
    IconLabelComponent,
    BannerComponent,
    FaqOrganizationsComponent,
    OrganizationContactComponent,
    OrganizationComponent,
    OfficeComponent,
    FaqVolunteersComponent,
  ],
  imports: [
    BrowserModule.withServerTransition({ appId: 'volontulo' }),
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    NgbModule.forRoot(),
    RouterModule.forRoot(appRoutes),
    CookieModule.forRoot()
  ],
  providers: [
    AuthService,
    OffersService,
    OrganizationService,
    { provide: WindowService, useFactory: WindowFactory },
    { provide: ErrorHandler, useClass: RavenErrorHandler },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
