import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CamerasComponent } from './cameras/cameras.component'
import { PersonsComponent } from './persons/persons.component'
import { TracksComponent } from './tracks/tracks.component'
import { HomeComponent } from './home/home.component'
import { PersonComponent } from './person/person.component'
import { CameraComponent } from './camera/camera.component'

 
const routes: Routes = [
  { path: 'cameras', component: CamerasComponent},
  { path: 'persons', component: PersonsComponent},
  { path: 'tracks', component: TracksComponent},
  { path: 'home', component: HomeComponent},
  { path: 'person/:id', component: PersonComponent},
  { path: 'camera/:id', component: CameraComponent},
  { path: '', redirectTo: '/home', pathMatch: 'full'},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
