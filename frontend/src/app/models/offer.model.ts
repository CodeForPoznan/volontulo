import { Organization } from 'app/models/organization.model';

export class Offer {
    actionOngoing: boolean;
    actionStatus: string;
    benefits: string;
    constantCoop: boolean;
    description: string;
    finishedAt: string | null;
    id: number;
    image: string;
    joined: boolean;
    location: string;
    offerStatus: string;
    organization: Organization;
    recruitmentEndDate: string | null;
    recruitmentStartDate: string | null;
    requirements: string;
    reserveRecruitment: boolean;
    reserveRecruitmentEndDate: string | null;
    reserveRecruitmentStartDate: string | null;
    reserveVolunteersLimit: number;
    slug: string;
    startedAt: string | null;
    timeCommitment: string;
    title: string;
    url: string;
    volunteersLimit: number;
}
