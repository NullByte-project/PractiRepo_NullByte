import { Component } from '@angular/core';
import { DocumentRequest } from 'src/app/model/document-request.model';
import { Practice } from 'src/app/model/practice.model';
import { UserModel } from 'src/app/model/user.model';
import { NotificaconesService } from 'src/app/servicios/notificacones.service';
import { ServicioLogicaService } from 'src/app/servicios/servicio-logica.service';
import { UserService } from 'src/app/servicios/user.service';

@Component({
  selector: 'app-dashboard-admin',
  templateUrl: './dashboard-admin.component.html',
  styleUrls: ['./dashboard-admin.component.css']
})
export class DashboardAdminComponent {
  stats = {
    totalPractices: 0,
    pendingRequests: 0,
    approvedRequests: 0,
    userCount: 0
  };

  recentPractices: any[] = [];
  pendingRequests: any[] = [];
  isAdmin = false;

  constructor(
    private userService: UserService,
    private practiceService: ServicioLogicaService,
    private documentRequestService: NotificaconesService
  ) { }

  async ngOnInit() {
    await this.loadStats();
    this.loadRecentPractices();
    this.checkAdminStatus();
    setInterval(() => this.loadPendingRequests(), 30000); // Actualizar cada 30 seg
  }

  async loadStats() {
    try {
      const [practices, requests, users] = await Promise.all([
        this.practiceService.getPractices().toPromise() as Promise<Practice[]>,
        this.documentRequestService.getDocumentRequests().toPromise() as Promise<DocumentRequest[]>,
        this.userService.getAllUsers().toPromise() as Promise<UserModel[]>
      ]);

      this.stats = {
        totalPractices: practices?.length ?? 0,
        pendingRequests: (requests?.filter(r => r.status === 'pending') || []).length,
        approvedRequests: (requests?.filter(r => r.status === 'approved') || []).length,
        userCount: users?.length ?? 0
      };
    } catch (error) {
      console.error('Error loading stats:', error);
      this.stats = {
        totalPractices: 0,
        pendingRequests: 0,
        approvedRequests: 0,
        userCount: 0
      };
    }
  }

  loadRecentPractices() {
    this.practiceService.getPractices().subscribe({
      next: (data) => this.recentPractices = data.slice(-5),
      error: (err) => console.error(err)
    });
  }

  loadPendingRequests() {
    if (this.isAdmin) {
      this.documentRequestService.getDocumentRequests('PENDING').subscribe({
        next: (data) => this.pendingRequests = data,
        error: (err) => console.error(err)
      });
    }
  }

  checkAdminStatus() {
    this.userService.getProfile().subscribe({
      next: (user) => this.isAdmin = user.role?.toLowerCase().includes('admin'),
      error: (err) => console.error(err)
    });
  }

}
