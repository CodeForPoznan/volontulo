import { Organization } from '../organization/organization.model';

export class Offer {
    id: number;
    image: string;
    location: string;
    organization: Organization;
    slug: string;
    startedAt: string | null;
    finishedAt: string | null;
    title: string;
    url: string;
}
