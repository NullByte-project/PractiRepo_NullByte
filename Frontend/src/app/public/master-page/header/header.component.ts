import { ChangeDetectorRef, Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/servicios/auth.service';



@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {

  isMenuOpen = false;

  constructor(
    public authService: AuthService,
    private router: Router,
    private cdRef: ChangeDetectorRef
  ) { }

  toggleMenu(): void {
    this.isMenuOpen = !this.isMenuOpen;
    this.cdRef.detectChanges(); // Forzar actualización de la vista
  }

  logout(): void {
    this.authService.logout();
    this.isMenuOpen = false;
    this.router.navigate(['/auth/login']);
  }

  // Cerrar menú al hacer clic fuera
  onDocumentClick(event: MouseEvent): void {
    if (!(event.target as HTMLElement).closest('.user-menu-container')) {
      this.isMenuOpen = false;
      this.cdRef.detectChanges();
    }
  }
}
