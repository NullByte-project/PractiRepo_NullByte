import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './public/home/home.component';
import { PageNotFoundComponent } from './public/errors/page-not-found/page-not-found.component';
import { ListPracticesComponent } from './module/practices/list-practices/list-practices.component';

const routes: Routes = [
  {
    path: 'home',
    component: HomeComponent
  },
  {
    path: '',
    pathMatch: 'full',
    redirectTo: '/home'
  },
  {
    path: 'auth',
    loadChildren : () => import('./module/auth/auth.module').then(m => m.AuthModule)
  },
  {
    path: 'practices',
    loadChildren : () => import('./module/practices/practices.module').then(m => m.PracticesModule)
  },
  {
    path: '**',
    component: PageNotFoundComponent
  }
  

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
