import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PracticeLoadComponent } from './practice-load.component';

describe('PracticeLoadComponent', () => {
  let component: PracticeLoadComponent;
  let fixture: ComponentFixture<PracticeLoadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PracticeLoadComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PracticeLoadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
