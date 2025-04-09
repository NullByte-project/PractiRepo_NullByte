import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PracticePreviewComponent } from './practice-preview.component';

describe('PracticePreviewComponent', () => {
  let component: PracticePreviewComponent;
  let fixture: ComponentFixture<PracticePreviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PracticePreviewComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PracticePreviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
