import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Practice } from 'src/app/model/practice.model';
import { ServicioLogicaService } from 'src/app/servicios/servicio-logica.service';

@Component({
  selector: 'app-list-practices',
  templateUrl: './list-practices.component.html',
  styleUrls: ['./list-practices.component.css']
})
export class ListPracticesComponent {
  p: number = 1;
  practices: Practice[] = [];
  filteredPractices: Practice[] = [];
  isLoading = true;
  filterForm: FormGroup;

  constructor(
    private servicioLogica: ServicioLogicaService,
    private fb: FormBuilder
  ) {
    this.filterForm = this.fb.group({
      title: [''],
      year: [''],
      practice_type: [''],
      institution: [''],
      author: [''],
      municipality: ['']
    });
  }

  ngOnInit() {
    this.loadPractices();
    this.setupFilterListeners();
  }

  loadPractices(filters?: any): void {
    this.isLoading = true;
    this.servicioLogica.getPractices(filters).subscribe({
      next: (data) => {
        console.log(data)
        this.practices = data;
        this.filteredPractices = [...data];
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Error loading practices:', err);
        this.isLoading = false;
      }
    });
  }

  setupFilterListeners(): void {
    this.filterForm.valueChanges.subscribe(() => {
      this.applyFilters();
    });
  }

  applyFilters(): void {
    const filters = this.filterForm.value;
    this.loadPractices(filters);
  }

  resetFilters(): void {
    this.filterForm.reset();
    this.loadPractices();
  }
}