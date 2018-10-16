import { NgModule } from '@angular/core';
import { ServerModule } from '@angular/platform-server';
import { ModuleMapLoaderModule } from '@nguniversal/module-map-ngfactory-loader';
import { CookieService, CookieBackendService } from 'ngx-cookie';

import { AppModule } from 'app/app.module';
import { AppComponent } from 'app/app.component';

@NgModule({
  imports: [
    // The AppServerModule should import your AppModule followed
    // by the ServerModule from @angular/platform-server.
    AppModule,
    ServerModule,
    ModuleMapLoaderModule,
  ],
  providers: [{ provide: CookieService, useClass: CookieBackendService }],
  // Since the bootstrapped component is not inherited from your
  // imported AppModule, it needs to be repeated here.
  bootstrap: [AppComponent],
})
export class AppServerModule {}
