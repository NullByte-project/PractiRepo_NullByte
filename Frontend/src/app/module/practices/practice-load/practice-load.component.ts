import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ServicioLogicaService } from 'src/app/servicios/servicio-logica.service';

@Component({
  selector: 'app-practice-load',
  templateUrl: './practice-load.component.html',
  styleUrls: ['./practice-load.component.css']
})
export class PracticeLoadComponent {
  practiceForm: FormGroup;
  isLoading = false;
  errorMessage = '';
  successMessage = '';

  constructor(
    private fb: FormBuilder,
    private servicio: ServicioLogicaService,
    public router: Router
  ) {
    this.practiceForm = this.fb.group({
      title: ['', [Validators.required, Validators.minLength(3)]],
      year: [new Date().getFullYear(), [Validators.required, Validators.min(2000)]],
      practice_type: ['', Validators.required],
      institution: [''],
      author: [''],
      municipality: [''],
      file: [null, Validators.required]
    });
  }

  onFileChange(event: any) {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      this.practiceForm.patchValue({
        file: file
      });
    }
  }

  onSubmit() {
    if (this.practiceForm.invalid) {
      this.errorMessage = 'Por favor complete todos los campos requeridos';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    const formData = new FormData();
    formData.append('title', this.practiceForm.get('title')?.value);
    formData.append('year', this.practiceForm.get('year')?.value);
    formData.append('practice_type', this.practiceForm.get('practice_type')?.value);
    formData.append('file', this.practiceForm.get('file')?.value);

    // Campos opcionales
    if (this.practiceForm.get('institution')?.value) {
      formData.append('institution', this.practiceForm.get('institution')?.value);
    }
    if (this.practiceForm.get('author')?.value) {
      formData.append('author', this.practiceForm.get('author')?.value);
    }
    if (this.practiceForm.get('municipality')?.value) {
      formData.append('municipality', this.practiceForm.get('municipality')?.value);
    }

    this.servicio.createPractice(formData).subscribe({
      next: (response) => {
        this.isLoading = false;
        this.successMessage = 'Práctica creada exitosamente';
        setTimeout(() => {
          this.router.navigate(['/practices']);
        }, 1500);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.error?.message || 'Error al crear la práctica';
        console.error('Error:', err);
      }
    });
  }
}
