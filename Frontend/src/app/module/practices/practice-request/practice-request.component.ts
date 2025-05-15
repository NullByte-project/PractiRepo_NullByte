import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NotificaconesService } from 'src/app/servicios/notificacones.service';

@Component({
  selector: 'app-practice-request',
  templateUrl: './practice-request.component.html',
  styleUrls: ['./practice-request.component.css']
})
export class PracticeRequestComponent {

  practiceId!: string;
  isLoading = false;

  ngOnInit(): void {
    this.practiceId = this.route.snapshot.paramMap.get('id')!;
  }

  constructor(
    private route: ActivatedRoute,
    private practiceService: NotificaconesService,
    public router: Router,

  ) { }
  submitRequest() {
    this.isLoading = true;
    this.practiceService.createDocumentRequest(this.practiceId).subscribe({
      next: () => {
        alert('Solicitud enviada exitosamente');
        this.router.navigate(['/practices/list-practices']);
      },
      error: (err) => {
        this.isLoading = false;
        alert(err.error?.detail || 'Error al enviar la solicitud');
      }
    });
  }

}
