import { Component, OnInit, AfterViewInit, Renderer2, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location} from '@angular/common';

import { Person } from '../_models/persons';
import { Tracks } from '../_models/tracks';
import { Router } from '@angular/router';

import { PersonsService } from '../_services/persons.service'
import { TracksService } from '../_services/tracks.service'

import { ImagesService } from '../_services/images.service'
import { Image, Imagess } from '../_models/images';

import { FormGroup, FormBuilder,FormArray, Validators, FormControl } from '@angular/forms';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-person',
  templateUrl: './person.component.html',
  styleUrls: ['./person.component.css']
})
export class PersonComponent implements OnInit, AfterViewInit {
  cards = [{'img': '../../assets/white.png'}];
  
  slides: any = [[]];

  signUpForm: FormGroup;
  deleteForm: FormGroup;

  isBusy = false;
  hasFailed = false;
  isSigned = false;
  message: string;

  person: Person;
  tracks: Tracks;
  personId: string;
  IMAGE_URL = environment.imageUrl;


  constructor(private route: ActivatedRoute,
    private router: Router,
    private location: Location,
    private personsService: PersonsService,
    private tracksService: TracksService,
    private imagesService: ImagesService,
    private formBuilder: FormBuilder,
    private renderer: Renderer2
    ) { }

  chunk(arr: any, chunkSize: number) {
    let R = [];
    for (let i = 0, len = arr.length; i < len; i += chunkSize) {
      R.push(arr.slice(i, i + chunkSize));
    }
    return R;
  }

  ngOnInit() {
    
    const id = this.route.snapshot.paramMap.get('id');
    this.personId = id
    this.getImages(this.personId)
    this.getPerson(id);
    this.getTracks(id);
    
    this.signUpForm = this.formBuilder.group({
      firstName: ['', Validators.required],
      lastName: ['',Validators.required],
      age: ['', [Validators.pattern("^(0|[1-9][0-9]*)$")]],
      height: ['', [Validators.pattern("^(0|[1-9][0-9]*)$")]],
      description: [''],
    });

    this.deleteForm = this.formBuilder.group({
    });
  }

  ngAfterViewInit() {
    const buttons = document.querySelectorAll('.btn-floating');
    buttons.forEach((el: any) => {
      this.renderer.removeClass(el, 'btn-floating');
      this.renderer.addClass(el, 'px-3');
      this.renderer.addClass(el.firstElementChild, 'fa-3x');
    });
  }


  @ViewChild('fileInput', {static: false}) fileInput;
  uploadFile() {
    const files: FileList = this.fileInput.nativeElement.files;
    if (files.length === 0) {
      return;
    };

    this.imagesService.addImage(files, this.personId).subscribe((data: any) => {
      this.getImages(this.personId)
    });
  }

  getImages(id: string) {
    this.imagesService.getImages(id).subscribe((images: Imagess) => {
      this.cards = images['images']
      
      if (images['images'].length == 0) {
        this.cards = [{'img': '../../assets/white.png'}];
      }
      
      this.slides = this.chunk(this.cards, 10);
    });
  }
  

  get f() { return this.signUpForm.controls; }
  get g() { return this.deleteForm.controls; }


  onSubmit() {
    // Reset status
   this.isBusy = true;
   this.hasFailed = false;

   const PERSON: Person = {
    id: this.personId,
    firstName: this.signUpForm.value.firstName,
    lastName: this.signUpForm.value.lastName,
    age: this.signUpForm.value.age,
    height: this.signUpForm.value.height,
    description: this.signUpForm.value.description
  }


  this.personsService
      .editPerson(PERSON)
      .subscribe(
        (response) => {
          this.getPerson(this.personId)
          this.router.navigate(['/person/' + this.personId]);
        },
        (error) => {
          this.isBusy = false;
          this.hasFailed = true;
        }
      );
  }

  onDelete() {
  this.personsService
      .deletePerson(this.personId)
      .subscribe(
        (response) => {
          this.router.navigate(['/persons']);
        },
        (error) => {
          this.isBusy = false;
          this.hasFailed = true;
        }
      );
  }

  getPerson(id: string): void {
    this.personsService.getPerson(id)
      .subscribe(person => {
        // console.log(person)
        this.person = person['person']
        this.signUpForm.controls['firstName'].setValue(this.person.firstName)
        this.signUpForm.controls['lastName'].setValue(this.person.lastName)
        this.signUpForm.controls['age'].setValue(this.person.age)
        this.signUpForm.controls['height'].setValue(this.person.height)
        this.signUpForm.controls['description'].setValue(this.person.description)
      }
      )
  }

  getTracks(personId: string): void {
    this.tracksService.getTracksForPerson(personId)
    .subscribe(tracks => {
      this.tracks = tracks
    }
    )
  }

  headElements = ['فرد', 'تاریخ', 'ساعت', 'ورود/خروج', 'دوربین'];

  goBack(): void {
    this.location.back();
  }

}
