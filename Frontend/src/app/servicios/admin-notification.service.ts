import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';
import { HttpClient } from '@angular/common/http';
import { configuracionRutasBackend } from '../config/configuracion-rutas';

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

  updateRequestStatus(requestId: string, newStatus: string, adminNotes?: string) {
    return this.http.put(
      `${this.apiUrl}/document-requests/admin/manage/${requestId}`,
      { status: newStatus, admin_notes: adminNotes },
      {
        headers: {
          Authorization: `Bearer ${this.authService.getToken()}`
        }
      }
    );
  }


}
