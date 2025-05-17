import { Injectable } from '@angular/core';
import { configuracionRutasBackend } from '../config/configuracion-rutas';
import { HttpClient, HttpParams } from '@angular/common/http';
import { catchError, Observable, of } from 'rxjs';
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
  // En tu NotificacionesService
getDocumentRequests(status?: string): Observable<any[]> {
  const params = status ? new HttpParams().set('status', status) : new HttpParams();
  return this.http.get<any[]>(`${this.apiUrl}/admin/all`, { params }).pipe(
    catchError(error => {
      console.error('Error obteniendo solicitudes:', error);
      return of([]); // Retorna array vacío en caso de error
    })
  );
}
  
  
  
  
  
  

  
}
