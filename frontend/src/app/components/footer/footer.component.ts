import { Component } from '@angular/core';

import { environment } from 'environments/environment';

@Component({
  selector: 'volontulo-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent {

  djangoRoot: string;

  constructor () {
    this.djangoRoot = environment.djangoRoot;
  }
}
