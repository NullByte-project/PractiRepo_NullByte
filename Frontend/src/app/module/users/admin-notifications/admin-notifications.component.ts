import { Component } from '@angular/core';
import { DocumentRequestStatus } from 'src/app/model/document-request.model';
import { AdminNotificationService } from 'src/app/servicios/admin-notification.service';

@Component({
  selector: 'app-admin-notifications',
  templateUrl: './admin-notifications.component.html',
  styleUrls: ['./admin-notifications.component.css']
})
export class AdminNotificationsComponent {
  requests: any[] = [];
  filteredRequests: any[] = [];
  selectedStatus: string = 'pending';
  isLoading = true;
  DocumentRequestStatus = DocumentRequestStatus;
  selectedRequest: any = null;
  adminNotes: string = '';

  statusOptions = [
    { value: 'pending', label: 'Pendientes' },
    { value: 'approved', label: 'Aprobadas' },
    { value: 'rejected', label: 'Rechazadas' }
  ];

  constructor(private notificationService: AdminNotificationService) { }

  ngOnInit(): void {
    this.loadRequests();
  }

  loadRequests(): void {
    this.isLoading = true;
    this.notificationService.getDocumentRequests(this.selectedStatus).subscribe({
      next: (data) => {
        this.requests = data;
        this.filteredRequests = [...data];
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Error loading requests:', err);
        this.isLoading = false;
        alert('Error cargando solicitudes');
      }
    });
  }

  onStatusFilterChange(): void {
    this.loadRequests();
  }

  prepareReject(request: any): void {
    this.selectedRequest = request;
    this.adminNotes = '';
  }

  cancelReject(): void {
    this.selectedRequest = null;
    this.adminNotes = '';
  }

  updateRequestStatus(request: any, newStatus: DocumentRequestStatus): void {
    const confirmationMessage = newStatus === DocumentRequestStatus.APPROVED
      ? '¿Está seguro que desea aprobar esta solicitud?'
      : '¿Está seguro que desea rechazar esta solicitud?';

    if (!confirm(confirmationMessage)) return;

    const notes = newStatus === DocumentRequestStatus.REJECTED ? this.adminNotes : null;

    this.notificationService.updateRequestStatus(request._id, newStatus).subscribe({
      next: (updatedRequest) => {
        const index = this.requests.findIndex(req => req._id === request._id);
        if (index !== -1) {
          // Actualizar la solicitud en ambas listas
          this.requests[index] = updatedRequest;
          this.filteredRequests = this.requests.filter(req =>
            this.selectedStatus === 'all' ? true : req.status === this.selectedStatus
          );
        }
        this.selectedRequest = null;
        this.adminNotes = '';
        alert(`Solicitud ${newStatus === DocumentRequestStatus.APPROVED ? 'aprobada' : 'rechazada'} correctamente`);
      },
      error: (err) => {
        console.error('Error actualizando solicitud:', err);
        alert('Error procesando la solicitud');
      }
    });
  }
}