import { Component, Inject, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

import { MetatagsService } from 'app/services/metatags.service';
import { WindowService } from 'app/services/window.service';
import { environment } from 'environments/environment';

@Component({
  selector: 'volontulo-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  constructor(
    @Inject(WindowService) private window: any,
    private metatagsService: MetatagsService,
    private router: Router
  ) { }

  ngOnInit() {
    this.window.ga('create', environment.googleAnalyticsAppID, 'auto');
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.metatagsService.setMeta();

        this.window.ga('set', 'page', event.urlAfterRedirects);
        this.window.ga('send', 'pageview');
      }
    });
  }

}
