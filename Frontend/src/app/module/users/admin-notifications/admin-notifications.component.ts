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
      }
    });
  }

  updateRequestStatus(requestId: string, newStatus: DocumentRequestStatus, notes?: string): void {
    this.notificationService.updateRequestStatus(requestId, newStatus, notes).subscribe({
      next: (updatedRequest) => {
        const index = this.requests.findIndex(req => req.id === requestId);
        if (index !== -1) {
          this.requests[index] = updatedRequest;
          this.filteredRequests = [...this.requests];
        }
      },
      error: (err) => {
        console.error('Error updating request:', err);
      }
    });
  }

  onStatusFilterChange(): void {
    this.loadRequests();
  }
  

}
