import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ContactFormComponent } from './contact-form/contact-form.component';
import { UserListComponent } from './user-list/user-list.component';
import { UserProfileComponent } from './user-profile/user-profile.component';
import { AdminNotificationsComponent } from './admin-notifications/admin-notifications.component';

const routes: Routes = [
  {
    path: 'contact-form',
    component: ContactFormComponent
  },
  {
    path: 'user-list',
    component: UserListComponent
  },
  {
    path: 'user-profile',
    component: UserProfileComponent
  },
  {
    path: 'admin-notifications',
    component: AdminNotificationsComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UsersRoutingModule { 





}


