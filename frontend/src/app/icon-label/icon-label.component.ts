import { Component, Input } from '@angular/core';

@Component({
  selector: 'volontulo-icon-label',
  templateUrl: './icon-label.component.html',
  styleUrls: ['./icon-label.component.css'],
})
export class IconLabelComponent {
  @Input() icon: string;

}
