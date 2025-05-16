import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { configuracionRutasBackend } from '../config/configuracion-rutas';
import { throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AdminNotificationService {

  apiUrl: string = configuracionRutasBackend.urlLogica;

  constructor(
    private http: HttpClient,
    private authService: AuthService

  ) { }

  getDocumentRequests(status?: string) {
    const headers = {
      Authorization: `Bearer ${this.authService.getToken()}`
    };

    let url = `${this.apiUrl}/document-requests/admin/all`;
    if (status) {
      url += `?status=${status}`;
    }

    return this.http.get<any[]>(url, { headers });
  }

  // En admin-notification.service.ts
  updateRequestStatus(requestId: string, status: string, adminNotes?: string) {
    const token = this.authService.getToken();

    // Verificar token
    if (!token) {
      console.error('Token no encontrado');
      return throwError(() => 'Usuario no autenticado');
    }

    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'  // Añadir explícitamente
    });

    const payload = { status, admin_notes: adminNotes || null };
    const url = `${this.apiUrl}/document-requests/admin/manage/${requestId}`;

    console.log('Enviando PUT a:', url); // Verificar URL en consola
    console.log('Payload:', payload);

    return this.http.put(url, payload, { headers });
  }

}
