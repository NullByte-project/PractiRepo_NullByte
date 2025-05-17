import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserService } from 'src/app/servicios/user.service';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})
export class UserProfileComponent {
 user: any = {};
  editMode = false;
  passwordData = {
    current: '',
    new: '',
    confirm: ''
  };
  isLoading = true;
  message = '';

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.loadProfile();
  }

  async loadProfile() {
    try {
      this.user = await this.userService.getProfile().toPromise();
      this.isLoading = false;
    } catch (error) {
      this.showMessage('Error cargando perfil');
    }
  }

  toggleEdit() {
    this.editMode = !this.editMode;
  }

  async updateProfile() {
    try {
      await this.userService.updateProfile(this.user).toPromise();
      this.showMessage('Perfil actualizado');
      this.editMode = false;
    } catch (error) {
      this.showMessage('Error actualizando perfil');
    }
  }

  async changePassword() {
    if (this.passwordData.new !== this.passwordData.confirm) {
      this.showMessage('Las contraseñas no coinciden');
      return;
    }
    
    try {
      await this.userService.changePassword(
        this.passwordData.current,
        this.passwordData.new
      ).toPromise();
      
      this.showMessage('Contraseña actualizada');
      this.passwordData = { current: '', new: '', confirm: '' };
    } catch (error) {
      this.showMessage('Error cambiando contraseña');
    }
  }

  showMessage(text: string) {
    this.message = text;
    setTimeout(() => this.message = '', 3000);
  }  
  
  
  

}
