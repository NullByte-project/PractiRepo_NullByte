import { Injectable } from '@angular/core';
import { configuracionRutasBackend } from '../config/configuracion-rutas';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from './auth.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  urlUser: string = configuracionRutasBackend.urlLogica + '/users';

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) { }

  // Métodos existentes
  getUser(): string {
    return localStorage.getItem('user') || '';
  }

  setUser(user: string): void {
    localStorage.setItem('user', user);
  }

  private getHeaders() {
    return new HttpHeaders({
      'Authorization': `Bearer ${this.authService.getToken()}`
    });
  }

  getAllUsers() {
    return this.http.get<any[]>(this.urlUser, { headers: this.getHeaders() });
  }

  deleteUser(userId: string) {
    return this.http.delete(`${this.urlUser}/${userId}`, { 
      headers: this.getHeaders(),
      responseType: 'text' 
    });
  }

  updateUser(userId: string, updateData: any) {
    return this.http.put(`${this.urlUser}/${userId}`, updateData, { 
      headers: this.getHeaders() 
    });
  }

  // Nuevos métodos para el perfil
  getProfile(): Observable<any> {
    return this.http.get(`${this.urlUser}/mi-perfil`, { headers: this.getHeaders() });
  }

  updateProfile(profileData: any): Observable<any> {
    return this.http.put(`${this.urlUser}/mi-perfil`, profileData, { 
      headers: this.getHeaders() 
    });
  }

  changePassword(currentPassword: string, newPassword: string): Observable<any> {
    return this.http.post(`${this.urlUser}/change-password`, {
      currentPassword,
      newPassword
    }, { headers: this.getHeaders() });
  }
}