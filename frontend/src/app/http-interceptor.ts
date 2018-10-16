import { HttpRequest, HttpInterceptor, HttpHandler, HttpEvent, HttpXsrfTokenExtractor } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';

import { environment } from 'environments/environment';


@Injectable()
export class HttpWithCredentialsInterceptor implements HttpInterceptor {

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    let authReq = req;
    if (req.url.startsWith(environment.apiRoot)) {
      authReq = req.clone({ withCredentials: true });
    }
    return next.handle(authReq);
  }
}

@Injectable()
export class HttpXsrfInterceptor implements HttpInterceptor {

  constructor(private tokenService: HttpXsrfTokenExtractor) { }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const headerName = 'x-csrftoken';
    const token = this.tokenService.getToken() as string;
    if (token !== null && !req.headers.has(headerName) && req.url.startsWith(environment.apiRoot)) {
      req = req.clone({ headers: req.headers.set(headerName, token) });
    }
    return next.handle(req);
  }
}
