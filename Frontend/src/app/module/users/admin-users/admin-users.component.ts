import { Component } from '@angular/core';
import { AuthService } from 'src/app/servicios/auth.service';
import { UserService } from 'src/app/servicios/user.service';

@Component({
  selector: 'app-admin-users',
  templateUrl: './admin-users.component.html',
  styleUrls: ['./admin-users.component.css']
})
export class AdminUsersComponent {

   users: any[] = [];
  isLoading = true;
  errorMessage = '';
  selectedUser: any = null;
  editData: any = {};
  roles: any[] = []; // Asumiendo que tienes un servicio para obtener roles

  constructor(
    private userService: UserService,
    private authService: AuthService
  ) { }

  ngOnInit() {
    this.loadUsers();
    this.loadRoles(); // Implementar este método si es necesario
  }

  loadUsers() {
    this.userService.getAllUsers().subscribe({
      next: (data) => {
        this.users = data;
        this.isLoading = false;
      },
      error: (err) => {
        this.errorMessage = 'Error cargando usuarios';
        this.isLoading = false;
      }
    });
  }

  loadRoles() {
    // Implementar llamada al backend para obtener roles
    this.roles = [
      { _id: '68202de33cdc4c141a30c0f4', name: 'Usuario' },
      { _id: '68202de33cdc4c141a30c0f5', name: 'Administrador' }
    ];
  }

  confirmDelete(user: any) {
    if (confirm(`¿Eliminar usuario "${user.email}"?`)) {
      this.deleteUser(user.id);
    }
  }

  deleteUser(id: string) {
    this.userService.deleteUser(id).subscribe({
      next: () => {
        this.users = this.users.filter(u => u.id !== id);
      },
      error: (err) => {
        this.errorMessage = 'Error eliminando usuario';
      }
    });
  }

  startEdit(user: any) {
    this.selectedUser = user;
    this.editData = { ...user };
    this.editData.role_id = user.role_id?._id || user.role_id;
  }

  cancelEdit() {
    this.selectedUser = null;
    this.editData = {};
  }

  updateUser() {
    this.userService.updateUser(this.selectedUser.id, this.editData)
      .subscribe({
        next: (updated) => {
          const index = this.users.findIndex(u => u.id === this.selectedUser.id);
          this.users[index] = updated;
          this.selectedUser = null;
        },
        error: (err) => {
          this.errorMessage = 'Error actualizando usuario';
        }
      });
  }

}
