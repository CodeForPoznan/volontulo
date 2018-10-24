import { Location } from '@angular/common';
import { Inject, Injectable } from '@angular/core';
import { Meta, Title } from '@angular/platform-browser';
import { ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

import { environment } from 'environments/environment';

@Injectable()
export class MetatagsService {

  constructor(
    private locationService: Location,
    private metaService: Meta,
    private titleService: Title
  ) { }

  public getCanonicalUrl(url: string): string {
    return Location.joinWithSlash(environment.angularRoot, url);
  }

  public setMeta(title = 'Volontulo. Portal dla wolontariuszy', metatags = {}): void {
    this.titleService.setTitle(title);

// set default tags, that will be orverwritten below:
    this.metaService.updateTag({ property: 'og:url', content: this.getCanonicalUrl(this.locationService.path()) });
    this.metaService.updateTag({ property: 'og:title', content: 'Volontulo. Portal dla wolontariuszy' });
    this.metaService.updateTag({ property: 'og:description', content: 'Volontulo. Portal dla wolontariuszy'});
    this.metaService.updateTag({ property: 'og:image', content: this.getCanonicalUrl('/assets/img/banner/volontulo_baner.png') });
    this.metaService.updateTag({ property: 'fb:app_id', content: environment.fbAppID });

    Object.keys(metatags)
      .map((key) => ({ property: key, content: metatags[key] }))
      .forEach((metatag) => this.metaService.updateTag(metatag));
  }
}
