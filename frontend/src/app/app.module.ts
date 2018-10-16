import { registerLocaleData, Location } from '@angular/common';
import { HTTP_INTERCEPTORS, HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import localePl from '@angular/common/locales/pl';
import { ErrorHandler, NgModule, PLATFORM_ID, LOCALE_ID } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule, Routes } from '@angular/router';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CookieModule } from 'ngx-cookie';
import * as Raven from 'raven-js';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IMaskModule } from 'angular-imask';

import { AppComponent } from 'app/app.component';
import { AccountComponent} from 'app/components/account/account.component';
import { ActivationComponent } from 'app/components/activation/activation.component';
import { BannerComponent } from 'app/components/banner/banner.component';
import { ContactComponent } from 'app/components/contact/contact.component';
import { CookieLawBannerComponent } from 'app/components/cookie-law-banner/cookie-law-banner.component';
import { FooterComponent } from 'app/components/footer/footer.component';
import { FormErrorComponent } from 'app/components/form-error/form-error.component';
import { HeaderComponent } from 'app/components/header/header.component';
import { HomePageComponent } from 'app/components/homepage/homepage.component';
import { HomepageOfferComponent } from 'app/components/homepage-offer/homepage-offer.component';
import { LoginComponent } from 'app/components/login/login.component';
import { MessagesComponent } from 'app/components/messages/messages.component';
import { CreateOfferComponent } from 'app/components/offers/create-offer/create-offer.component';
import { OfferDetailComponent } from 'app/components/offers/offer-detail/offer-detail.component';
import { OrganizationComponent } from 'app/components/organization/organization.component';
import { OrganizationContactComponent } from 'app/components/organization/organization-contact/organization-contact.component';
import { OrganizationDetailsComponent } from 'app/components/organization/organization-details/organization-details.component';
import { OrganizationOffersListComponent } from 'app/components/organization/organization-offers-list/organization-offers-list.component';
import { OrganizationsComponent } from 'app/components/organizations/organizations.component';
import { OrganizationCreateComponent } from 'app/components/organization/organization-create/organization-create.component';
import { OrganizationsListComponent } from 'app/components/organizations/organizations-list/organizations-list.component';
import { PasswordResetComponent } from 'app/components/password-reset/password-reset.component';
import { PasswordResetConfirmComponent } from 'app/components/password-reset/password-reset-confirm.component';
import { RedirectComponent } from 'app/components/redirect/redirect.component';
import { RegisterComponent } from 'app/components/register/register.component';
import { AboutUsComponent } from 'app/components/static/about-us.component';
import { FaqOrganizationsComponent } from 'app/components/static/faq-organizations.component';
import { FaqVolunteersComponent } from 'app/components/static/faq-volunteers.component';
import { OfficeComponent } from 'app/components/static/office/office.component';
import { RegulationsComponent } from 'app/components/static/regulations.component';
import { UserProfileComponent } from 'app/components/user-profile/user-profile.component';
import { LoggedInGuard } from 'app/guards/loggedInGuard.service';
import { LoggedOutGuard } from 'app/guards/loggedOutGuard.service';
import { HttpWithCredentialsInterceptor, HttpXsrfInterceptor } from 'app/http-interceptor';
import { ContactResolver } from 'app/resolvers';
import { AuthService } from 'app/services/auth.service';
import { ContactService } from 'app/services/contact.service';
import { MessagesService } from 'app/services/messages.service';
import { MetatagsService } from 'app/services/metatags.service';
import { OffersService } from 'app/services/offers.service';
import { OrganizationService } from 'app/services/organization.service';
import { UserService } from 'app/services/user.service';
import { WindowFactory, WindowService } from 'app/services/window.service';
import { environment } from 'environments/environment';

Raven.config(environment.sentryDSN).install();

class RavenErrorHandler implements ErrorHandler {
  handleError(err: any): void {
    Raven.captureException(err);
  }
}

export function ErrorHandlerFactory(): ErrorHandler {
  return environment.production ? new RavenErrorHandler() : new ErrorHandler();
}

const appRoutes: Routes = [
  {
    path: '',
    component: HomePageComponent,
  },
  {
    path: 'organizations/:organizationSlug/:organizationId/edit',
    component: OrganizationCreateComponent,
    canActivate: [LoggedInGuard],
  },
  {
    path: 'organizations/:organizationSlug/:organizationId',
    component: OrganizationComponent,

  },
  {
    path: 'organizations/create',
    component: OrganizationCreateComponent,
    canActivate: [LoggedInGuard],
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
    component: AboutUsComponent,
  },
  {
    path: 'login',
    component: LoginComponent,
    canActivate: [LoggedOutGuard],
  },
  {
    path: 'register',
    component: RegisterComponent,
  },
  {
    path: 'activate/:token',
    component: ActivationComponent
  },
  {
    path: 'regulations',
    component: RegulationsComponent,
  },
  {
    path: 'offers/:offerSlug/:offerId',
    component: OfferDetailComponent,
  },
  {
    path: 'offers/create',
    component: CreateOfferComponent,
    canActivate: [LoggedInGuard],
  },
  {
    path: 'offers/:offerSlug/:offerId/edit',
    component: CreateOfferComponent,
    canActivate: [LoggedInGuard],
  },
  {
    path: 'organizations',
    component: OrganizationsComponent,
  },
  {
    path: 'password-reset/:uidb64/:token',
    component: PasswordResetConfirmComponent,
  },
  {
    path: 'password-reset',
    component: PasswordResetComponent,
    canActivate: [LoggedOutGuard],
  },
  {
    // change path from "/me-working-path" to "/me" when the whole user view is ready
    path: 'me-working-path',
    component: AccountComponent,
    canActivate: [LoggedInGuard]
  },
  {
    path: 'contact',
    component: ContactComponent,
    resolve: {
      contactData: ContactResolver,
    },
  },
  {
    path: 'me',
    component: UserProfileComponent,
    canActivate: [LoggedInGuard],
  },
  {
    path: '**',
    component: RedirectComponent
  },
  {
    path: '**',
    component: RedirectComponent,
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
    BannerComponent,
    OrganizationsComponent,
    FaqOrganizationsComponent,
    OrganizationContactComponent,
    OrganizationComponent,
    OfficeComponent,
    FaqVolunteersComponent,
    CreateOfferComponent,
    PasswordResetComponent,
    PasswordResetConfirmComponent,
    MessagesComponent,
    OrganizationOffersListComponent,
    RegisterComponent,
    ActivationComponent,
    OrganizationCreateComponent,
    OrganizationsListComponent,
    AccountComponent,
    ContactComponent,
    FormErrorComponent,
    OrganizationsListComponent,
    UserProfileComponent
  ],
  imports: [
    BrowserModule.withServerTransition({ appId: 'volontulo' }),
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({ cookieName: 'csrftoken' }),
    NgbModule.forRoot(),
    RouterModule.forRoot(appRoutes),
    CookieModule.forRoot(),
    ReactiveFormsModule,
    FontAwesomeModule,
    IMaskModule,
  ],
  providers: [
    MetatagsService,
    AuthService,
    OffersService,
    OrganizationService,
    MessagesService,
    UserService,
    LoggedInGuard,
    LoggedOutGuard,
    ContactResolver,
    ContactService,
    Location,
    { provide: LOCALE_ID, useValue: 'pl' },
    { provide: WindowService, useFactory: WindowFactory, deps: [PLATFORM_ID] },
    { provide: ErrorHandler, useFactory: ErrorHandlerFactory },
    { provide: HTTP_INTERCEPTORS, useClass: HttpWithCredentialsInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: HttpXsrfInterceptor, multi: true },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
