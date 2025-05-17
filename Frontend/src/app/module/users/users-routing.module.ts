import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ContactFormComponent } from './contact-form/contact-form.component';
import { UserListComponent } from './user-list/user-list.component';
import { UserProfileComponent } from './user-profile/user-profile.component';
import { AdminNotificationsComponent } from './admin-notifications/admin-notifications.component';
import { AdminGuard } from 'src/app/guards/admin.guard';
import { AuthGuard } from 'src/app/guards/auth.guard';
import { AdminUsersComponent } from './admin-users/admin-users.component';
import { DashboardAdminComponent } from './dashboard-admin/dashboard-admin.component';

const routes: Routes = [
  {
    path: 'contact-form',
    component: ContactFormComponent
  },
  {
    path: 'user-list',
    component: UserListComponent,
    canActivate: [AdminGuard]
  },
  {
    path: 'user-profile',
    component: UserProfileComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'admin-notifications',
    component: AdminNotificationsComponent,
    canActivate: [AdminGuard]
  },
  {
    path: 'admin-users',
    component: AdminUsersComponent,
    canActivate: [AdminGuard]
  },{
    path: 'dashboard-admin',
    component: DashboardAdminComponent,
    canActivate: [AdminGuard]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UsersRoutingModule { 





}


