import { Injectable } from '@angular/core';
import { configuracionRutasBackend } from '../config/configuracion-rutas';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class NotificaconesService {

  urlcontacto: string = configuracionRutasBackend.urlLogica + '/email';
  apiUrl: string = configuracionRutasBackend.urlLogica + '/document-requests';

  constructor(private http: HttpClient, private authService: AuthService) { }
  enviarFormularioContacto(data: any): Observable<any> {
    return this.http.post(this.urlcontacto + '/contact', data);
  }

  createDocumentRequest(practiceId: string) {
    return this.http.post(`${this.apiUrl}/request/${practiceId}`, {}, {
      headers: {
        Authorization: `Bearer ${this.authService.getToken()}`
      }
    });


  }
}
