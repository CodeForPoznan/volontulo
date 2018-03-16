import { ErrorHandler, NgModule, PLATFORM_ID, LOCALE_ID } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule, Routes } from '@angular/router';
import { registerLocaleData } from '@angular/common';
import localePl from '@angular/common/locales/pl';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CookieModule } from 'ngx-cookie';
import * as Raven from 'raven-js';
import { HTTP_INTERCEPTORS, HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';

import { environment } from '../environments/environment';
import { OffersService } from './homepage-offer/offers.service';
import { AppComponent } from './app.component';
import { RedirectComponent } from './redirect.component';
import { WindowFactory, WindowService } from './window.service';
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
import { MessagesComponent } from './messages/messages.component';
import { OrganizationsComponent } from './organizations/organizations.component';
import { HttpWithCredentialsInterceptor, HttpXsrfInterceptor } from './http-interceptor';
import { FaqOrganizationsComponent } from './static/faq-organizations.component';
import { OrganizationContactComponent } from './organization/organization-contact/organization-contact.component';
import { OrganizationComponent } from './organization/organization.component';
import { OfficeComponent } from './static/office/office.component';
import { FaqVolunteersComponent } from './static/faq-volunteers.component';
import { PasswordResetComponent } from './password-reset/password-reset.component';
import { PasswordResetConfirmComponent } from './password-reset/password-reset-confirm.component';
import { OrganizationOffersListComponent } from './organization/organization-offers-list/organization-offers-list.component';

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
    path: 'organizations',
    component: OrganizationsComponent
  },
  {
    path: 'password-reset/:uidb64/:token',
    component: PasswordResetConfirmComponent,
  },
  {
    path: 'password-reset',
    component: PasswordResetComponent,
  },
  {
    path: '**',
    component: RedirectComponent
  },
];

registerLocaleData(localePl);

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
    OrganizationsComponent,
    FaqOrganizationsComponent,
    OrganizationContactComponent,
    OrganizationComponent,
    OfficeComponent,
    FaqVolunteersComponent,
    PasswordResetComponent,
    PasswordResetConfirmComponent,
    MessagesComponent,
    OrganizationOffersListComponent,
  ],
  imports: [
    BrowserModule.withServerTransition({ appId: 'volontulo' }),
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({ cookieName: 'csrftoken' }),
    NgbModule.forRoot(),
    RouterModule.forRoot(appRoutes),
    CookieModule.forRoot()
  ],
  providers: [
    AuthService,
    OffersService,
    OrganizationService,
    { provide: LOCALE_ID, useValue: 'pl' },
    { provide: WindowService, useFactory: WindowFactory, deps: [PLATFORM_ID] },
    { provide: ErrorHandler, useClass: RavenErrorHandler },
    { provide: HTTP_INTERCEPTORS, useClass: HttpWithCredentialsInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: HttpXsrfInterceptor, multi: true },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
