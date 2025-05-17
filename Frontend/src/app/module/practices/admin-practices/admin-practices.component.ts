import { Component } from '@angular/core';
import { AuthService } from 'src/app/servicios/auth.service';
import { ServicioLogicaService } from 'src/app/servicios/servicio-logica.service';

@Component({
  selector: 'app-admin-practices',
  templateUrl: './admin-practices.component.html',
  styleUrls: ['./admin-practices.component.css']
})
export class AdminPracticesComponent {
  practices: any[] = [];
  isLoading = true;
  errorMessage = '';
  selectedPractice: any = null;
  editData: any = {};

  constructor(
    private practiceService: ServicioLogicaService,
    private authService: AuthService
  ) { }

  ngOnInit() {
    this.loadPractices();
  }

  loadPractices() {
    this.practiceService.getAllPractices().subscribe({
      next: (data) => {
        this.practices = data;
        this.isLoading = false;
      },
      error: (err) => {
        this.errorMessage = 'Error cargando prácticas';
        this.isLoading = false;
      }
    });
  }

  confirmDelete(practice: any) {
    if (confirm(`¿Eliminar práctica "${practice.title}"?`)) {
      this.deletePractice(practice.id);
    }
  }

  deletePractice(id: string) {
    this.practiceService.deletePractice(id).subscribe({
      next: () => {
        this.practices = this.practices.filter(p => p.id !== id);
      },
      error: (err) => {
        this.errorMessage = 'Error eliminando práctica';
      }
    });
  }

  startEdit(practice: any) {
    this.selectedPractice = practice;
    this.editData = { ...practice };
  }

  cancelEdit() {
    this.selectedPractice = null;
    this.editData = {};
  }

  updatePractice() {
    this.practiceService.updatePractice(this.selectedPractice.id, this.editData)
      .subscribe({
        next: (updated) => {
          const index = this.practices.findIndex(p => p.id === this.selectedPractice.id);
          this.practices[index] = updated;
          this.selectedPractice = null;
        },
        error: (err) => {
          this.errorMessage = 'Error actualizando práctica';
        }
      });
  }

}
