import { Component, Input } from '@angular/core';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'volontulo-form-error',
  templateUrl: './form-error.component.html',
  styleUrls: ['./form-error.component.scss']
})
export class FormErrorComponent {
  @Input() fc: FormControl;
  @Input() minLength: number;
  @Input() maxLength: number;
  @Input() customError: string;
}
