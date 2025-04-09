import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ListPracticesComponent } from './list-practices/list-practices.component';
import { PracticeUploadComponent } from './practice-upload/practice-upload.component';
import { PracticePreviewComponent } from './practice-preview/practice-preview.component';

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
    path: 'practice-preview',
    component: PracticePreviewComponent
  },
  {
    path: 'practice-upload',
    component: PracticeUploadComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PracticesRoutingModule { }
