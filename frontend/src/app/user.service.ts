import { Injectable } from '@angular/core';
import { Headers, Http, Response, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Rx';

@Injectable()
export class UserService {
  private url = 'http://localhost:8000/api/login';

  constructor(private http: Http) {
  }

  loginUser(username: string, password: string) {
    const headers: Headers = new Headers({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    });
    const options: RequestOptions = new RequestOptions({ headers: headers });

    return this.http.post(this.url, { username, password }, options)
      .map((res: Response) => res.json())
      .catch(this.handleError);
  }

  handleError(reject: Response | any) {
    const body = reject.json() || '';
    const err = body.error || JSON.stringify(body);
    console.log(err);
    return Observable.throw(err);
  }
}
