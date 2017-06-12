import { Component, Inject, OpaqueToken } from '@angular/core';
import { Router } from '@angular/router';

import { environment } from '../environments/environment';

export const WindowToken = new OpaqueToken('Window');

export function _window(): Window {
  return window;
}

@Component({
  template: ''
})
export class RedirectComponent {
  constructor(
    private router: Router,
    @Inject(WindowToken) private window: any
  ) {
    const angularUrlSuffix = this.router.routerState.snapshot.url;
    const djangoUrlSuffix = angularUrlSuffix === '/' ? '' : angularUrlSuffix;
    this.window.location.href = `${environment.djangoRoot}${djangoUrlSuffix}`;
  }
}
