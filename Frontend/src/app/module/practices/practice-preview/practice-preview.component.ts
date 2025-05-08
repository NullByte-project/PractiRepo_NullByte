import { Component, OnInit } from '@angular/core';
import { Practice } from 'src/app/model/practice.model';
import { PreviewFragment } from 'src/app/model/preview.model';
import { ActivatedRoute } from '@angular/router';
import { ServicioLogicaService } from 'src/app/servicios/servicio-logica.service';

@Component({
  selector: 'app-practice-preview',
  templateUrl: './practice-preview.component.html',
  styleUrls: ['./practice-preview.component.css']
})
export class PracticePreviewComponent implements OnInit {
  practiceId: string = '';
  practice?: Practice;
  fragments: PreviewFragment[] = [];
  isLoading = true;
  errorMessage = '';

  constructor(
    private route: ActivatedRoute,
    private practiceService: ServicioLogicaService
  ) { }

  ngOnInit(): void {
    this.practiceId = this.route.snapshot.paramMap.get('id') || '';
    this.loadPracticeAndPreview();
  }

  loadPracticeAndPreview(): void {
    this.isLoading = true;

    // Primero cargar los datos básicos de la práctica
    this.practiceService.getPractices(this.practiceId).subscribe({
      next: (practices) => {
        this.practice = practices.find(p => p.id === this.practiceId);
        if (this.practice) {
          // Luego cargar el preview
          this.loadPreview();
        } else {
          this.isLoading = false;
          this.errorMessage = 'Práctica no encontrada';
        }
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = 'Error al cargar la práctica';
        console.error(err);
      }
    });
  }

  loadPreview(): void {
    this.practiceService.getPreview(this.practiceId).subscribe({
      next: (fragments) => {
        this.fragments = fragments;
        this.isLoading = false;
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = 'No se pudo cargar la previsualización del documento';
        console.error(err);
      }
    });
  }

  getFileIcon(): string {
    if (!this.practice) return 'description';
    const type = this.practice.practice_type.toLowerCase();
    if (type.includes('pdf')) return 'picture_as_pdf';
    if (type.includes('word')) return 'description';
    if (type.includes('excel')) return 'table_chart';
    return 'insert_drive_file';
  }

}
