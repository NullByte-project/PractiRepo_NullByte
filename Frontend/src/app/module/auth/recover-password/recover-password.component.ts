import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from 'src/app/servicios/auth.service';

@Component({
  selector: 'app-recover-password',
  templateUrl: './recover-password.component.html',
  styleUrls: ['./recover-password.component.css']
})
export class RecoverPasswordComponent {

   resetForm: FormGroup;
  isLoading = false;
  message = '';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService
  ) {
    this.resetForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]]
    });
  }

  onSubmit() {
    if (this.resetForm.invalid) return;

    this.isLoading = true;
    this.message = '';

    this.authService.resetPassword(this.resetForm.value.email).subscribe({
      next: () => {
        this.message = 'Si el correo existe, recibirás una contraseña temporal';
        this.resetForm.reset();
      },
      error: (err) => {
        this.message = 'Error al procesar la solicitud';
        console.error(err);
      },
      complete: () => this.isLoading = false
    });
  }

}
