import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PracticeUploadComponent } from './practice-upload.component';

describe('PracticeUploadComponent', () => {
  let component: PracticeUploadComponent;
  let fixture: ComponentFixture<PracticeUploadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PracticeUploadComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PracticeUploadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
