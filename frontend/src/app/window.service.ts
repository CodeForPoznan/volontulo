import { InjectionToken } from '@angular/core';


export const WindowService = new InjectionToken<Window>('Window');

export function WindowFactory(): Window {
  return window;
}
