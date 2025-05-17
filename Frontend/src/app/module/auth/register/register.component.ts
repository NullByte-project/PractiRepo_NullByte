import { HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { UserModel, UserRegisterModel } from 'src/app/model/user.model';
import { AuthService } from 'src/app/servicios/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {

  isSubmitting = false;
  errorMessage = '';
  successMessage = '';
  registroForm: FormGroup;

  constructor(private fb: FormBuilder, private authService: AuthService, private router: Router) {
    this.registroForm = this.fb.group({
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', Validators.required],
      tipoUsuario: ['externo', Validators.required],
      aceptaTerminos: [false, Validators.requiredTrue]
    }, {
      validators: this.passwordMatchValidator
    });
  }

  passwordMatchValidator(form: FormGroup) {
    const password = form.get('password')?.value;
    const confirmPassword = form.get('confirmPassword')?.value;

    if (password !== confirmPassword) {
      form.get('confirmPassword')?.setErrors({ passwordMismatch: true });
      return { passwordMismatch: true };
    }

    return null;
  }


  async onSubmit() {
    if (this.registroForm.valid) {
      this.isSubmitting = true;
      this.errorMessage = '';

      try {
        const formValue = this.registroForm.value;

        const userData: UserRegisterModel = {
          first_name: formValue.nombre,
          last_name: formValue.apellido,
          email: formValue.email,
          password: formValue.password,
          role_id: this.getRoleId(formValue.tipoUsuario)
        };

        await this.authService.register(userData);
        this.handleSuccess();
      } catch (error) {
        this.handleError(error as HttpErrorResponse);
      } finally {
        this.isSubmitting = false;
      }
    } else {
      this.markFormAsTouched();
    }
  }

  private getRoleId(tipoUsuario: string): string {
    return tipoUsuario === 'estudiante'
      ? '68202de33cdc4c141a30c0f5'  
      : '68202e043cdc4c141a30c0f5'; 
  }

  private handleSuccess() {
    this.successMessage = '¡Registro exitoso! Por favor inicia sesión';
    setTimeout(() => {
      this.router.navigate(['/auth/login']);
    }, 2000);
  }

  private handleError(error: HttpErrorResponse) {
    if (error.status === 400 && error.error?.detail) {
      this.errorMessage = error.error.detail;
    } else {
      this.errorMessage = 'Error al conectar con el servidor';
    }
  }

  private markFormAsTouched() {
    Object.keys(this.registroForm.controls).forEach(key => {
      this.registroForm.get(key)?.markAsTouched();
    });
  }











  get nombre() { return this.registroForm.get('nombre'); }
  get apellido() { return this.registroForm.get('apellido'); }
  get email() { return this.registroForm.get('email'); }
  get password() { return this.registroForm.get('password'); }
  get confirmPassword() { return this.registroForm.get('confirmPassword'); }
  get tipoUsuario() { return this.registroForm.get('tipoUsuario'); }
  get aceptaTerminos() { return this.registroForm.get('aceptaTerminos'); }

}
