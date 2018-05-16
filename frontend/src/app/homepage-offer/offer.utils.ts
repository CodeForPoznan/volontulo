import { ApiOffer } from './offers.model';

export function loadDefaultImage(offer: ApiOffer): ApiOffer {
    if (!offer.image) {
        offer.image = 'assets/img/banner/volontulo_baner.png';
    }
    return offer;
  }
