import { Component, OnInit } from '@angular/core';
import {Persons, Person} from '../_models/persons';
import { FormGroup, FormBuilder,FormArray, Validators, FormControl } from '@angular/forms';
import { Router } from '@angular/router';

import { PersonsService } from '../_services/persons.service'
import { ImagesService } from '../_services/images.service'
import { AllImages } from '../_models/images';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-persons',
  templateUrl: './persons.component.html',
  styleUrls: ['./persons.component.css']
})
export class PersonsComponent implements OnInit {
  allImages;
  currentPage: number = 1;
  pageSize: number = 9;

  signUpForm: FormGroup;
  isBusy = false;
  hasFailed = false;
  isSigned = false;
  message: string;

  persons: Persons;

  IMAGE_URL = environment.imageUrl;

  constructor(private formBuilder: FormBuilder,
    private router: Router,
    private personsService: PersonsService,
    private imagesService: ImagesService,

    ) {

  }
  ngOnInit() {
    this.signUpForm = this.formBuilder.group({
      firstName: ['', Validators.required],
      lastName: ['',Validators.required],
      age: ['', [Validators.pattern("^(0|[1-9][0-9]*)$")]],
      height: ['', [Validators.pattern("^(0|[1-9][0-9]*)$")]],
      description: [''],
    });
    this.getPersons()
    this.getAllImages()
  }

  getAllImages(): void {
    this.imagesService.getAllImages()
      .subscribe(allImages => {
        this.allImages = allImages['images']
      }
      )
  }

  getPersons(): void {
    this.personsService.getPersons()
      .subscribe(persons => {
        this.persons = persons
      }
      )
  }

  updatePate(pageNumber: number): void {
    this.currentPage = pageNumber
  }

  get f() { return this.signUpForm.controls; }

  onSubmit() {
   this.isBusy = true;
   this.hasFailed = false;

   const PERSON: Person = {
    id: '-1',
    firstName: this.signUpForm.value.firstName,
    lastName: this.signUpForm.value.lastName,
    age: this.signUpForm.value.age,
    height: this.signUpForm.value.height,
    description: this.signUpForm.value.description
  }


  this.personsService
      .addPerson(PERSON)
      .subscribe(
        (response) => {
          this.getPersons()
          this.router.navigate(['/persons']);
        },
        (error) => {
          this.isBusy = false;
          this.hasFailed = true;
        }
      );
 }

  getPerson(personId: string) {
    this.router.navigate(['/person/' + personId])
  }

}
