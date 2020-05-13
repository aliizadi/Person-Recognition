import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { Image, Imagess, AllImages } from '../_models/images';
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
export class ImagesService {

  constructor(private http: HttpClient) { }
  
  addImage(files: FileList, personId: string) {
      const formData: FormData = new FormData();
      formData.append('file', files[0], files[0].name);
      return this.http.post(API_URL + '/persons/images/' + personId, formData);
  }

  getImages(personId: string){
    return this.http.get<Imagess>(API_URL + '/persons/images/' + personId , httpOptions)
      .pipe(
        catchError(error => {
            return throwError(error)
          }
        )
      )
  }

  getAllImages(){
    return this.http.get<AllImages>(API_URL + '/persons/all/images', httpOptions)
      .pipe(
        catchError(error => {
            return throwError(error)
          }
        )
      )
  }
}
