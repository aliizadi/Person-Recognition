import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { Person, Persons } from '../_models/persons';
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
export class PersonsService {

  constructor(private http: HttpClient) { }

  addPerson(PERSON: Person) {
    return this.http.post<Person>(API_URL + '/persons' , PERSON, httpOptions)
    .pipe(
      catchError(error => error)
    );
  }

  getPersons(){
    return this.http.get<Persons>(API_URL + '/persons', httpOptions)
      .pipe(
        catchError(error => {
            return throwError(error)
          }
        )
      )
  }

  getPerson(id: string){
    return this.http.get<Person>(API_URL + '/persons/profile/' + id, httpOptions)
      .pipe(
        catchError(error => {
            return throwError(error)
          }
        )
      )
  }

  editPerson(PERSON: Person){
    return this.http.put<Person>(API_URL + '/persons', PERSON, httpOptions)
      .pipe(
        catchError(error => {
            return throwError(error)
          }
        )
      )
  }

  deletePerson(id: string){
    return this.http.delete<Person>(API_URL + '/persons/' + id, httpOptions)
      .pipe(
        catchError(error => {
            return throwError(error)
          }
        )
      )
  }

}
