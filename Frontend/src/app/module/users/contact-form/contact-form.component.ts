import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { NotificaconesService } from 'src/app/servicios/notificacones.service';

@Component({
  selector: 'app-contact-form',
  templateUrl: './contact-form.component.html',
  styleUrls: ['./contact-form.component.css']
})
export class ContactFormComponent {
  contactForm: FormGroup;
  success: string | null = null;
  error: string | null = null;

  constructor(private fb: FormBuilder, private notificacionesService: NotificaconesService) {
    this.contactForm = this.fb.group({
      nombre: ['', Validators.required],
      apellidos: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      telefono: [''],
      mensaje: ['', Validators.required],
      terminos: [false, Validators.requiredTrue],
      tipoUsuario: ['', Validators.required]
    });
  }

  onSubmit() {
    if (this.contactForm.valid) {
      this.notificacionesService.enviarFormularioContacto(this.contactForm.value)
        .subscribe({
          next: (res) => {
            this.success = 'Formulario enviado con éxito.';
            this.error = null;
            this.contactForm.reset();
          },
          error: (err) => {
            this.success = null;
            this.error = 'Hubo un error al enviar el formulario.';
          }
        });


    } else {
      this.success = null;
      this.error = 'Por favor complete todos los campos obligatorios.';
    }
  }
}
