import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { configuracionRutasBackend } from '../config/configuracion-rutas';
import { Observable } from 'rxjs';
import { Practice } from '../model/practice.model';
import { PreviewFragment } from '../model/preview.model';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class ServicioLogicaService {

  urlLogica: string = configuracionRutasBackend.urlLogica;
  urlPractices: string = configuracionRutasBackend.urlLogica + '/practices';
  urlPreview = configuracionRutasBackend.urlLogica + '/previews';

  constructor(private http: HttpClient, private authService: AuthService) { }

  // getPractices(): Observable<Practice[]> {
  // return this.http.get<Practice[]>(this.urlLogica + '/practices');
  // }
  getPractice(practiceId: string): Observable<Practice> {
    return this.http.get<Practice>(`${this.urlPractices}/${practiceId}`);
  }

  getPractices(filters?: any): Observable<Practice[]> {
    let params = new HttpParams();

    if (filters) {
      Object.keys(filters).forEach(key => {
        if (filters[key] !== null && filters[key] !== undefined && filters[key] !== '') {
          params = params.append(key, filters[key]);
        }
      });
    }

    return this.http.get<Practice[]>(this.urlPractices + '/filter', { params });
  }



  // createPractice(formData: FormData): Observable<Practice> {
    // return this.http.post<Practice>(this.urlPractices, formData);
  // }

  createPractice(formData: FormData) {
    // Obtener el token del AuthService
    const token = this.authService.getToken();
    
    // Crear headers con el token
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });

    return this.http.post(`${this.urlPractices}`, formData, { headers });
  }


  getPreview(practiceId: string): Observable<PreviewFragment[]> {
    return this.http.get<PreviewFragment[]>(`${this.urlPreview}/${practiceId}`);
  }

}
