import { NgModule } from '@angular/core';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { ChangePasswordComponent } from './change-password/change-password.component';
import { RecoverPasswordComponent } from './recover-password/recover-password.component';
import { AuthGuard } from 'src/app/guards/auth.guard';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
{
  path: 'register',
  component: RegisterComponent
},
{
  path: 'login',
  component: LoginComponent
},
{
  path: 'change-password',
  component: ChangePasswordComponent,
  canActivate: [AuthGuard]
},
{
  path: 'recover-password',
  component: RecoverPasswordComponent
}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AuthRoutingModule { }
