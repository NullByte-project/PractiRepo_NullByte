import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { configuracionRutasBackend } from '../config/configuracion-rutas';
import { UserModel } from '../model/user.model';
import { BehaviorSubject, catchError, tap, throwError } from 'rxjs';
import { Router } from '@angular/router';

interface LoginResponse {
  access_token: string;
  token_type: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private isAuthenticated = new BehaviorSubject<boolean>(false);
  private currentUser = new BehaviorSubject<any>(null);
  urlLogica: string = configuracionRutasBackend.urlLogica;
  urlusers: string = configuracionRutasBackend.urlLogica + '/users';

  constructor(private http: HttpClient, private router: Router) { }

  login(email: string, password: string) {
    return this.http.post<LoginResponse>(`${this.urlusers}/login`, { email, password }).pipe(
      tap(response => {
        this.handleAuthentication(response.access_token);
      }),
      catchError(this.handleError)
    );
  }

  private handleAuthentication(token: string) {
    localStorage.setItem('auth_token', token);
    this.isAuthenticated.next(true);
    this.router.navigate(['/home']);
    this.decodeAndSetUserData(token);
  }
  
  // En tu auth.service.ts, temporalmente:
private decodeAndSetUserData(token: string) {
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        console.log('Payload decodificado:', payload); // Para verificar en consola
        
        this.currentUser.next({
            email: payload.sub,
            role: payload.role,
            role_id: payload.role_id,
            permissions: payload.permissions
        });
        
    } catch (error) {
        console.error('Error decodificando token:', error);
    }
}

  getCurrentUser() {
    return this.currentUser.asObservable();
  }


  private handleError(errorRes: HttpErrorResponse) {
    let errorMessage = 'Error desconocido';

    // Ajusta según la estructura de errores de tu backend
    if (errorRes.error && errorRes.error.detail) {
      errorMessage = errorRes.error.detail;
    } else if (errorRes.status === 401) {
      errorMessage = 'Credenciales inválidas';
    }

    return throwError(() => new Error(errorMessage));
  }

  get isAuthenticated$() {
    return this.isAuthenticated.asObservable();
  }
  getToken() {
    return localStorage.getItem('auth_token');
  }
  logout() {
    localStorage.removeItem('auth_token');
    this.isAuthenticated.next(false);
    this.router.navigate(['/login']);
  }
  register(user: UserModel): Promise<any> {
    return this.http.post<any>(this.urlusers + '/register', user).toPromise();
  }
}