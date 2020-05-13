import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Camera } from '../_models/cameras';
import { Tracks } from '../_models/tracks'
import { Router } from '@angular/router';

import { CamerasService } from '../_services/cameras.service'
import { TracksService } from '../_services/tracks.service'

import { FormGroup, FormBuilder,FormArray, Validators, FormControl } from '@angular/forms';

@Component({
  selector: 'app-camera',
  templateUrl: './camera.component.html',
  styleUrls: ['./camera.component.css']
})
export class CameraComponent implements OnInit {

  signUpForm: FormGroup;
  deleteForm: FormGroup;

  isBusy = false;
  hasFailed = false;
  isSigned = false;
  message: string;

  camera: Camera;
  tracks: Tracks;
  cameraId: string;

  constructor(private route: ActivatedRoute,
    private location: Location,
    private camerasService: CamerasService,
    private tracksService: TracksService,
    private router: Router,
    private formBuilder: FormBuilder,
    ) { }

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id')
    this.cameraId = id
    this.getCamera(id)
    this.getTracks(id)
    this.signUpForm = this.formBuilder.group({
      name: ['', Validators.required],
      ip: ['',Validators.required],
      port: ['', [Validators.required, Validators.pattern("^(0|[1-9][0-9]*)$")]],
    });

    this.deleteForm = this.formBuilder.group({});
  }

  get f() { return this.signUpForm.controls; }
  get g() { return this.deleteForm.controls; }

  onSubmit() {

    // Reset status
    this.isBusy = true;
    this.hasFailed = false;
 
    const CAMERA: Camera = {
     id: this.cameraId,
     name: this.signUpForm.value.name,
     ip: this.signUpForm.value.ip,
     port: this.signUpForm.value.port
   }
 
 
   this.camerasService
       .editCamera(CAMERA)
       .subscribe(
         (response) => {
           this.getCamera(this.cameraId)
           this.router.navigate(['/camera/' + this.cameraId]);
         },
         (error) => {
           this.isBusy = false;
           this.hasFailed = true;
         }
       );
 }

 onDelete() {

 this.camerasService
     .deleteCamera(this.cameraId)
     .subscribe(
       (response) => {
         this.router.navigate(['/cameras']);
       },
       (error) => {
         this.isBusy = false;
         this.hasFailed = true;
       }
     );

}
  getCamera(id: string): void {

    this.camerasService.getCamera(id)
      .subscribe(camera => {
        // console.log(camera)
        this.camera = camera['camera']
        this.signUpForm.controls['name'].setValue(this.camera.name)
        this.signUpForm.controls['ip'].setValue(this.camera.ip)
        this.signUpForm.controls['port'].setValue(this.camera.port)
      }
      )
  }

  getTracks(cameraId: string): void {
    this.tracksService.getTracksForCamera(cameraId)
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
