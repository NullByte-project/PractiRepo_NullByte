import { Component } from '@angular/core';
import { Practice } from 'src/app/model/practice.model';
import { ServicioLogicaService } from 'src/app/servicios/servicio-logica.service';

@Component({
  selector: 'app-list-practices',
  templateUrl: './list-practices.component.html',
  styleUrls: ['./list-practices.component.css']
})
export class ListPracticesComponent {
  practices: Practice[] = [];
  isLoading = true;

  constructor(private servicioLogica: ServicioLogicaService) {}
  ngOnInit() {
    this.loadPractices();
  }
  loadPractices(): void {
    this.servicioLogica.getPractices().subscribe({
      next: (data) => {
        this.practices = data;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Error loading practices:', err);
        this.isLoading = false;
      }
    });
  }

}
