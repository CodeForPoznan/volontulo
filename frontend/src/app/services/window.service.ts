import { isPlatformBrowser } from '@angular/common';
import { InjectionToken } from '@angular/core';

interface FakeWindow {
  ga: () => any,
  setTimeout: (f: Function, t: number) => void,
  location: Object,
}

export const WindowService = new InjectionToken<Window>('Window');

export function WindowFactory(platformId: any): Window | FakeWindow {
  if (isPlatformBrowser(platformId)) {
    return window;
  } else {
    return  {
      ga: () => null,
      setTimeout: () => null,
      location: {},
    };
  }
}
