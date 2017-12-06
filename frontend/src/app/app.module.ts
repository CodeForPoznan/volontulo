import { ErrorHandler, NgModule } from '@angular/core';
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
import { HomepageOfferComponent } from './homepage-offer/homepage-offer.component';
import { HomePageComponent } from './home/homepage.component';
import { FooterComponent } from './footer/footer.component';
import { HeaderComponent } from './header/header.component';
import { CookieLawBannerComponent } from './cookie-law-banner/cookie-law-banner.component';
import { AboutUsComponent } from './static/about-us.component';
import { RegulationsComponent } from './static/regulations.component';
import { LoginComponent } from './login/login.component';
import { AuthService } from './auth.service';
import { BannerComponent } from './banner/banner.component';

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
    path: 'o-nas',
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
    HomepageOfferComponent,
    CookieLawBannerComponent,
    AboutUsComponent,
    RegulationsComponent,
    LoginComponent,
    BannerComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    NgbModule.forRoot(),
    RouterModule.forRoot(appRoutes),
    CookieModule.forRoot()
  ],
  providers: [
    AuthService,
    { provide: WindowService, useFactory: WindowFactory },
    { provide: ErrorHandler, useClass: RavenErrorHandler }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
