import { Component, OnInit } from '@angular/core';
import {Track, Tracks} from '../_models/tracks'
import {Person, Persons} from '../_models/persons'
import {Camera} from '../_models/cameras'
import { FormGroup, FormBuilder,FormArray, Validators, FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import { Location} from '@angular/common';

import { TracksService } from '../_services/tracks.service'
import { PersonsService } from '../_services/persons.service'
import { environment } from '../../environments/environment';


@Component({
  selector: 'app-tracks',
  templateUrl: './tracks.component.html',
  styleUrls: ['./tracks.component.css']
})
export class TracksComponent implements OnInit {
  currentPage: number = 1;
  pageSize: number = 5;
  searchText;
  signUpForm: FormGroup;
  isBusy = false;
  hasFailed = false;
  isSigned = false;
  message: string;

  tracks: Tracks;
  persons: Persons;
  headElements = ['فرد', 'تاریخ', 'ساعت', 'ورود/خروج', 'دوربین'];
  IMAGE_URL = environment.imageUrl;


  constructor(private formBuilder: FormBuilder,
    private tracksService: TracksService,
    private personsService: PersonsService,
    private route: ActivatedRoute,
    private router: Router,
    private location: Location,
    ) { }

  ngOnInit() {
    this.getTracks()
    this.getPersons()
    this.signUpForm = this.formBuilder.group({
      person: [null, Validators.required],
    });
  }

  getTracks(): void {
    this.tracksService.getTracks()
      .subscribe(tracks => {
        this.tracks = tracks
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

  get f() { return this.signUpForm.controls; }

  onSubmit(track: Track) {
   this.isBusy = true;
   this.hasFailed = false;

   const NEWTRACK: Track = {
    id: track.id,
    encoding_id: track.encoding_id,
    person: this.signUpForm.value.person,
    date: track.date,
    time: track.time,
    kind: track.kind,
    camera: track.camera,
    image: track.image
  }


  this.tracksService
      .editTrack(NEWTRACK)
      .subscribe(
        (response) => {
          this.getTracks()
          this.router.navigate(['/tracks']);
        },
        (error) => {
          this.isBusy = false;
          this.hasFailed = true;
        }
      );
  }

}
