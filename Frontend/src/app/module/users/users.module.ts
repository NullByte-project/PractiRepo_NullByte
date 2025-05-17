import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { UsersRoutingModule } from './users-routing.module';
import { UserListComponent } from './user-list/user-list.component';
import { ContactFormComponent } from './contact-form/contact-form.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { UserProfileComponent } from './user-profile/user-profile.component';
import { AdminNotificationsComponent } from './admin-notifications/admin-notifications.component';
import { AdminUsersComponent } from './admin-users/admin-users.component';
import { DashboardAdminComponent } from './dashboard-admin/dashboard-admin.component';


@NgModule({
  declarations: [
    UserListComponent,
    ContactFormComponent,
    UserProfileComponent,
    AdminNotificationsComponent,
    AdminUsersComponent,
    DashboardAdminComponent
  ],
  imports: [
    CommonModule,
    UsersRoutingModule,
     ReactiveFormsModule,
     FormsModule,
  ]
})
export class UsersModule { }
