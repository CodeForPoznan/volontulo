import { Image } from './image.model'
import { Organization } from '../organization/organization.model';

export class BaseOffer {
    id: number;
    joined: boolean;
    location: string;
    organization: Organization;
    slug: string;
    startedAt: string | null;
    finishedAt: string | null;
    title: string;
    url: string;
    recruitmentEndDate: string | null;
    timeCommitment: string;
    requirements: string;
    benefits: string;
    description: string;
    recruitmentStartDate: string | null;
    reserveRecruitment: boolean;
    reserveRecruitmentStartDate: string | null;
    reserveRecruitmentEndDate: string | null;
    actionOngoing: boolean;
    constantCoop: boolean;
    volunteersLimit: number;
    reserveVolunteersLimit: number;
    actionStatus: string;
    offerStatus: string;
}

export class ApiOffer extends BaseOffer {
    image: string;
}

export class AppOffer extends BaseOffer {
    image: Image | null;
}
