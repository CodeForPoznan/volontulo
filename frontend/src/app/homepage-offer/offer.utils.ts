import { Offer } from './offers.model';

export function loadDefaultImage(offer: Offer): Offer {
    if (!offer.image) {
        offer.image = 'assets/img/banner/volontulo_baner.png';
    }
    return offer;
  }
