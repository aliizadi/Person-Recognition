import { Component, OnInit } from '@angular/core';
import {Cameras, Camera} from '../_models/cameras';
import { FormGroup, FormBuilder,FormArray, Validators, FormControl } from '@angular/forms';

import { Router } from '@angular/router';
import { CamerasService } from '../_services/cameras.service'



@Component({
  selector: 'app-cameras',
  templateUrl: './cameras.component.html',
  styleUrls: ['./cameras.component.css']
})
export class CamerasComponent implements OnInit {
  currentPage: number = 1;
  pageSize: number = 9;

  signUpForm: FormGroup;
  isBusy = false;
  hasFailed = false;
  isSigned = false;
  message: string;

  cameras: Cameras = {
    cameras: [
      {
        id: '1',
        name: 'راهرو طبقه همکف',
        ip: '192.168.1.206',
        port: 8080
      }]
  }

 constructor(private formBuilder: FormBuilder,
  private router: Router,
  private camerasService: CamerasService,
  ) {

  }
  ngOnInit() {
    this.signUpForm = this.formBuilder.group({
      name: ['', Validators.required],
      ip: ['',Validators.required],
      port: ['', [Validators.required, Validators.pattern("^(0|[1-9][0-9]*)$")]],
    });
    this.getCameras()
  }

  getCameras(): void {
    this.camerasService.getCameras()
      .subscribe(cameras => {
        // console.log(persons)
        this.cameras = cameras
      }
      )
  }

  get f() { return this.signUpForm.controls; }

  onSubmit() {

    // Reset status
    this.isBusy = true;
    this.hasFailed = false;
 
    const CAMERA: Camera = {
     id: '-1',
     name: this.signUpForm.value.name,
     ip: this.signUpForm.value.ip,
     port: this.signUpForm.value.port
   }
 
 
   this.camerasService
       .addCamera(CAMERA)
       .subscribe(
         (response) => {
           this.getCameras()
           this.router.navigate(['/cameras']);
         },
         (error) => {
           this.isBusy = false;
           this.hasFailed = true;
         }
       );

 }

 getCamera(cameraId: string) {
  this.router.navigate(['/camera/' + cameraId])
}

}
