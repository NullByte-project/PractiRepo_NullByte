import { Injectable } from '@angular/core';
import { configuracionRutasBackend } from '../config/configuracion-rutas';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class NotificaconesService {

  urlcontacto: string = configuracionRutasBackend.urlLogica + '/email';
  
  constructor(private http: HttpClient) { }
  enviarFormularioContacto(data: any): Observable<any> {
    return this.http.post(this.urlcontacto + '/contact', data);
  }




}
