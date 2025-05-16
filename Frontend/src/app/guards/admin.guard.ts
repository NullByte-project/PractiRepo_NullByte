import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { AuthService } from '../servicios/auth.service';

@Injectable({
  providedIn: 'root'
})
export class AdminGuard implements CanActivate {

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean> {
    return this.authService.getCurrentUser().pipe(
      map(user => {
        const isAdmin = user?.role === 'admin';
        
        if (!isAdmin) {
          this.router.navigate(['/auth/login'], {
            queryParams: { 
              returnUrl: state.url,
              reason: 'admin_required'
            }
          });
          return false;
        }
        return true;
      }),
      catchError(() => {
        this.router.navigate(['/error', 'no-auth']);
        return [false];
      })
    );
  }
}