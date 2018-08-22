import { Injectable } from '@angular/core';
import { Meta, Title } from '@angular/platform-browser';

@Injectable()
export class MetatagsService {

  constructor(private MetaService: Meta, private TitleService: Title) { }

  public setMeta(title = 'Volontulo - Portal dla wolontariuszy', metatags = {}): void {
    this.TitleService.setTitle(title);


    Object.keys(metatags)
      .map((key) => ({name: key, content: metatags[key]}))
      .forEach((metatag) => this.MetaService.updateTag(metatag))
  }

}
