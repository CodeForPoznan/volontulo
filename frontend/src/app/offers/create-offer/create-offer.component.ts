import 'rxjs/add/operator/filter';
import 'rxjs/add/operator/do';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { Offer } from 'app/homepage-offer/offers.model';
import { AuthService } from 'app/auth.service';
import { User } from 'app/user';
import { OffersService } from 'app/homepage-offer/offers.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs/Subscription';
import { FileReaderEvent, FileReaderEventTarget } from '../../models';
import { FormGroup } from '@angular/forms';
import { FormBuilder } from '@angular/forms';
import { Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'volontulo-create-offer',
  templateUrl: './create-offer.component.html',
  styleUrls: ['./create-offer.component.scss']
})
export class CreateOfferComponent implements OnInit, OnDestroy {
  public hasOrganization = false;
  public inEditMode = false;
  public isAdmin = false;
  public isFileToBig = false;
  public offer: Offer = new Offer();
  public user: User;
  public userSubscription: Subscription;
  public form: FormGroup;
  public error;

  constructor(
    private authService: AuthService,
    private offersService: OffersService,
    private activatedRoute: ActivatedRoute,
    private fb: FormBuilder,
    private http: HttpClient,
    private router: Router,
  ) {}

  ngOnInit() {
    this.form = this.fb.group({
      title: ['', Validators.required],
      location: ['', Validators.required],
      organization: ['', Validators.required],
      startedAt: [],
      actionOngoing: [false],
      finishedAt: [],
      constantCoop: [false],
      recruitmentStartDate: [null],
      recruitmentEndDate: [null],
      volunteersLimit: [],
      reserveRecruitmentStartDate: [null],
      reserveRecruitmentEndDate: [null],
      reserveVolunteersLimit: [],
      description: ['', Validators.required],
      timeCommitment: ['', Validators.required],
      benefits: ['', Validators.required],
      requirements: [''],
      image: [],
    }, {validator: this.areDatesValid})

      this.userSubscription = this.authService.user$
      .subscribe(user => {
        if (user) {
          this.user = user;
          this.isAdmin = user['isAdministrator'];
          this.hasOrganization = user['organizations'].length > 0;
        }
     });

    this.activatedRoute.params
    .map(params => params.offerId)
    .filter(offerId => offerId !== undefined)
    .switchMap(offerId => this.offersService.getOffer(offerId))
    .do(offer => this.toDataUrl(offer.image))
    .subscribe((response: Offer) => {
      this.offer = response;
      this.inEditMode = true;
      this.form.patchValue(this.offer);
    });
  }

  ngOnDestroy() {
    if (this.userSubscription) {
      this.userSubscription.unsubscribe();
    };
  }

  private toDataUrl(url) {
    const reader = new FileReader();
    this.http.get(url, {responseType: 'blob'})
    .subscribe(response => {
      reader.onloadend = () => {
        this.offer.image = reader.result;
    }
      reader.readAsDataURL(response);
    })
  };

  onSubmit(offer: Offer) {
    if (!this.form.valid) {
      return
    }
    if (this.offer.image) {
      this.form.value.image = this.offer.image.replace(/.*,/, '');
    }
    if (this.inEditMode) {
      this.offersService.editOffer(this.form.value, offer.id)
      .subscribe(
        (response: Offer) => this.router.navigate(['offers/' + response.slug + '/' + response.id]),
        err => this.error = err.error.nonFieldErrors
    );
    } else {
      this.offersService.createOffer(this.form.value)
      .subscribe(
        (response: Offer) => this.router.navigate(['offers/' + response.slug + '/' + response.id]),
        err => this.error = err.error.nonFieldErrors
      );
    }
  }

  onFileSelected(event) {
    const reader = new FileReader();
    const file = event.target.files[0];
    reader.onloadend = (a: FileReaderEvent) => {
      if (file.size > 1048576) {
        return this.isFileToBig = true;
      }
      this.offer.image = (a.currentTarget as FileReaderEventTarget).result;
     }
    reader.readAsDataURL(file)
    this.isFileToBig = false;
  }

  isFormInputInvalid(inputStringId: string): boolean {
    const input = this.form.get(inputStringId);
    return !input.valid && input.touched || (this.error && !input.valid);
  }

  areDatesValid(form: FormGroup): {[key: string]: boolean} | null {
    const { startedAt, actionOngoing, finishedAt, constantCoop } = form.value;
    const validationErrors = {};

    if (startedAt && actionOngoing) {
      validationErrors['startedAtError'] = true;
    }

    if (finishedAt && constantCoop) {
      validationErrors['finishedAtError'] = true;
    }

    const hasAnyError = Object.keys(validationErrors).length > 0;

    return hasAnyError ? validationErrors : null;
  }
}
