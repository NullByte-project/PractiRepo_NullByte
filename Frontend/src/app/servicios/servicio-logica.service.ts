import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { configuracionRutasBackend } from '../config/configuracion-rutas';
import { Observable } from 'rxjs';
import { Practice } from '../model/practice.model';

@Injectable({
  providedIn: 'root'
})
export class ServicioLogicaService {

  urlLogica: string = configuracionRutasBackend.urlLogica;
  urlPractices: string = configuracionRutasBackend.urlLogica + '/practices';

  constructor(private http: HttpClient) { }

  getPractices(): Observable<Practice[]> {
    return this.http.get<Practice[]>(this.urlLogica + '/practices');
  }
  createPractice(formData: FormData): Observable<Practice> {
    return this.http.post<Practice>(this.urlPractices, formData);
  }

}
