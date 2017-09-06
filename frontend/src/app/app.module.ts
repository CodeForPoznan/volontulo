import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule, Routes } from '@angular/router';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AppComponent } from './app.component';
import { RedirectComponent } from './redirect.component';
import { WindowService, WindowFactory } from './window.service';
import { HomeComponent } from './home/home.component';
import { FooterComponent } from './footer/footer.component';
import { NavbarComponent } from './navbar/navbar.component';
import { SubFooterComponent } from './sub-footer/sub-footer.component';


const appRoutes: Routes = [
  // {
  //   path: '',
  //   component: HomeComponent
  // },
  {
    path: '**',
    component: RedirectComponent
  }
];

@NgModule({
  declarations: [
    AppComponent,
    RedirectComponent,
    HomeComponent,
    NavbarComponent,
    FooterComponent,
    SubFooterComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    NgbModule.forRoot(),
    RouterModule.forRoot(appRoutes)
  ],
  providers: [
    { provide: WindowService, useFactory: WindowFactory }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
