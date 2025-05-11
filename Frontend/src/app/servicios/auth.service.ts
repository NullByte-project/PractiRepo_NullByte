import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { configuracionRutasBackend } from '../config/configuracion-rutas';
import { UserModel } from '../model/user.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  urlLogica: string = configuracionRutasBackend.urlLogica;
  urlPractices: string = configuracionRutasBackend.urlLogica + '/auth';

  constructor(private http: HttpClient) { }

  register(user: UserModel): Promise<any> {
    return this.http.post<any>(this.urlPractices + '/register', user).toPromise();
  }
}
