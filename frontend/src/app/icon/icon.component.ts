import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

@Component({
  selector: 'volontulo-icon',
  templateUrl: './icon.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class IconComponent {
  @Input() content: string;
}
