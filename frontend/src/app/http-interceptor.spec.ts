import { HttpRequest } from '@angular/common/http';

import { HttpWithCredentialsInterceptor } from 'app/http-interceptor';
import { environment } from 'environments/environment';

class Handler {
  handle = jasmine.createSpy('handle');
}

describe('HttpInterceptor', () => {
  let handler;

  beforeEach(() => {
    handler = new Handler();
  });

  it('add credentials if request is to API', () => {
    const interceptor = new HttpWithCredentialsInterceptor();
    const request = new HttpRequest('GET', environment.apiRoot);
    interceptor.intercept(request, handler);

    expect(handler.handle).toHaveBeenCalledWith(request.clone({ withCredentials: true }));
  });

  it('pass request if it to an external service', () => {
    const interceptor = new HttpWithCredentialsInterceptor();
    const request = new HttpRequest('GET', `https://somepage.com?q=environment.apiRoot`);
    interceptor.intercept(request, handler);

    expect(handler.handle).toHaveBeenCalledWith(request);
  });
});
