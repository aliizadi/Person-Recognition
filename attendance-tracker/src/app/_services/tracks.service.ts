import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { Track, Tracks } from '../_models/tracks';
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
export class TracksService {

  constructor(private http: HttpClient) { }

  getTracks(){
    return this.http.get<Tracks>(API_URL + '/tracks', httpOptions)
      .pipe(
        catchError(error => {
            return throwError(error)
          }
        )
      )
  }

  getTrack(id: string){
    return this.http.get<Track>(API_URL + '/tracks/' + id, httpOptions)
      .pipe(
        catchError(error => {
            return throwError(error)
          }
        )
      )
  }

  getTracksForCamera(cameraId: string){
    return this.http.get<Tracks>(API_URL + '/cameras/tracks/' + cameraId, httpOptions)
      .pipe(
        catchError(error => {
            return throwError(error)
          }
        )
      )
  }

  getTracksForPerson(personId: string){
    return this.http.get<Tracks>(API_URL + '/persons/tracks/' + personId, httpOptions)
      .pipe(
        catchError(error => {
            return throwError(error)
          }
        )
      )
  }

  editTrack(TRACK: Track){
    return this.http.put<Track>(API_URL + '/tracks', TRACK, httpOptions)
      .pipe(
        catchError(error => {
            return throwError(error)
          }
        )
      )
  }

  deleteTrack(id: string){
    return this.http.delete<Track>(API_URL + '/tracks/' + id, httpOptions)
      .pipe(
        catchError(error => {
            return throwError(error)
          }
        )
      )
  }
}
