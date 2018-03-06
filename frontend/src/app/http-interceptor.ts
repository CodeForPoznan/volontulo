import { Injectable } from '@angular/core';
import { HttpRequest, HttpInterceptor as AngularHttpInterceptor, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { environment } from '../environments/environment';

@Injectable()
export class HttpInterceptor implements AngularHttpInterceptor {

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    let authReq = req;
    if (req.url.indexOf(environment.apiRoot) === 0) {
      authReq = req.clone({ withCredentials: true });
    }
    return next.handle(authReq);
  }
}
