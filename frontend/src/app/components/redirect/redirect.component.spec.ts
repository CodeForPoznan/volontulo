import { TestBed, async } from '@angular/core/testing';

import { RedirectComponent } from 'app/components/redirect/redirect.component';
import { environment } from 'environments/environment';


describe('RedirectComponent', () => {

  describe('for root url', () => {

    let redirect, routerStub, windowStub;

    beforeEach(async(() => {
      routerStub = { routerState: { snapshot: { url: '' } } };
      windowStub = { location: { href: 'http://testserver/' } };

      TestBed.configureTestingModule({
        providers: [
          { provide: 'Window', useValue: windowStub }
        ]
      });

      redirect = new RedirectComponent(routerStub, windowStub);
    }));

    it('should redirect without trailing slash', async(() => {
      expect(windowStub.location.href.slice(-1)).not.toEqual('/');
    }));

    it('should equal django root url', async(() => {
      expect(windowStub.location.href).toEqual(environment.djangoRoot);
    }));

  });

  describe('for sub-url', () => {

    let redirect, routerStub, windowStub;

    beforeEach(async(() => {
      routerStub = { routerState: { snapshot: { url: 'foo/bar?baz#foo' } } };
      windowStub = { location: { href: 'http://testserver/' } };

      TestBed.configureTestingModule({
        providers: [
          { provide: 'Window', useValue: windowStub }
        ]
      });

      redirect = new RedirectComponent(routerStub, windowStub);
    }));

    it('should redirect without trailing slash', async(() => {
      expect(windowStub.location.href.slice(-1)).not.toEqual('/');
    }));

    it('should contain django root url', async(() => {
      expect(windowStub.location.href.indexOf(environment.djangoRoot))
        .not.toEqual(-1);
    }));

    it('should contain sub-url suffix', async(() => {
      expect(windowStub.location.href
        .indexOf(routerStub.routerState.snapshot.url)).not.toEqual(-1);
    }));

  });

});
