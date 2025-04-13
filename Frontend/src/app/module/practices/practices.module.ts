import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { PracticesRoutingModule } from './practices-routing.module';
import { ListPracticesComponent } from './list-practices/list-practices.component';
import { PracticeUploadComponent } from './practice-upload/practice-upload.component';
import { PracticeDetailComponent } from './practice-detail/practice-detail.component';
import { PracticePreviewComponent } from './practice-preview/practice-preview.component';
import { PracticeLoadComponent } from './practice-load/practice-load.component';
import { ReactiveFormsModule } from '@angular/forms';
import { NgxPaginationModule } from 'ngx-pagination';


@NgModule({
  declarations: [
    ListPracticesComponent,
    PracticeUploadComponent,
    PracticeDetailComponent,
    PracticePreviewComponent,
    PracticeLoadComponent
  ],
  imports: [
    CommonModule,
    PracticesRoutingModule,
    ReactiveFormsModule,
    NgxPaginationModule
  ]
})
export class PracticesModule { }
