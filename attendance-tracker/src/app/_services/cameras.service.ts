import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { Camera, Cameras } from '../_models/cameras';
import { throwError } from 'rxjs';

const API_URL = environment.apiUrl;

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type':  'application/json'
  })
};

@Injectable({
  providedIn: 'root'
})
export class CamerasService {

  constructor(private http: HttpClient) { }

  addCamera(CAMERA: Camera) {
    return this.http.post<Camera>(API_URL + '/cameras' , CAMERA, httpOptions)
    .pipe(
      catchError(error => error)
    );
  }

  getCameras(){
    return this.http.get<Cameras>(API_URL + '/cameras', httpOptions)
      .pipe(
        catchError(error => {
            return throwError(error)
          }
        )
      )
  }

  getCamera(id: string){
    return this.http.get<Camera>(API_URL + '/cameras/inf/' + id, httpOptions)
      .pipe(
        catchError(error => {
            return throwError(error)
          }
        )
      )
  }

  editCamera(CAMERA: Camera){
    return this.http.put<Camera>(API_URL + '/cameras', CAMERA, httpOptions)
      .pipe(
        catchError(error => {
            return throwError(error)
          }
        )
      )
  }

  deleteCamera(id: string){
    return this.http.delete<Camera>(API_URL + '/cameras/' + id , httpOptions)
      .pipe(
        catchError(error => {
            return throwError(error)
          }
        )
      )
  }
}
