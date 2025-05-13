import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { UsersRoutingModule } from './users-routing.module';
import { UserListComponent } from './user-list/user-list.component';
import { ContactFormComponent } from './contact-form/contact-form.component';
import { ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    UserListComponent,
    ContactFormComponent
  ],
  imports: [
    CommonModule,
    UsersRoutingModule,
     ReactiveFormsModule,
  ]
})
export class UsersModule { }
