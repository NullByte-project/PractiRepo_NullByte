import { Injectable } from '@angular/core';
import { configuracionRutasBackend } from '../config/configuracion-rutas';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  urlUser: string = configuracionRutasBackend.urlLogica + '/user';

  constructor() { }

  getUser(): string {
    return localStorage.getItem('user') || '';
  }
  setUser(user: string): void {
    localStorage.setItem('user', user);
  }
}
