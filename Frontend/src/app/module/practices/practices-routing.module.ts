import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ListPracticesComponent } from './list-practices/list-practices.component';
import { PracticeUploadComponent } from './practice-upload/practice-upload.component';
import { PracticePreviewComponent } from './practice-preview/practice-preview.component';
import { PracticeLoadComponent } from './practice-load/practice-load.component';

const routes: Routes = [
  {
    path: 'list-practices',
    component: ListPracticesComponent
  },
  {
    path: 'practice-detail',
    component: PracticeUploadComponent
  },
  {
    path: 'practice-preview/:id',
    component: PracticePreviewComponent
  },
  {
    path: 'practice-upload',
    component: PracticeUploadComponent
  },
  {
    path: 'practice-load',
    component: PracticeLoadComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PracticesRoutingModule { }
