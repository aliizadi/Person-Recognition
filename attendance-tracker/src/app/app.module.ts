import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { MDBBootstrapModule } from 'angular-bootstrap-md';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { PersonsComponent } from './persons/persons.component';
import { PersonComponent } from './person/person.component';
import { TracksComponent } from './tracks/tracks.component';
import { CamerasComponent } from './cameras/cameras.component';
import { CameraComponent } from './camera/camera.component';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { Ng2SearchPipeModule } from 'ng2-search-filter';
import {NgxPaginationModule} from 'ngx-pagination';

import { PersonsService } from './_services/persons.service';
import { CamerasService } from './_services/cameras.service';
import { TracksService } from './_services/tracks.service';
import { ImagesService } from './_services/images.service';


@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    PersonsComponent,
    PersonComponent,
    TracksComponent,
    CamerasComponent,
    CameraComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    MDBBootstrapModule.forRoot(),
    Ng2SearchPipeModule,
    NgxPaginationModule
  ],
  providers: [
    PersonsService,
    CamerasService,
    TracksService,
    ImagesService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
