import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PracticeRequestComponent } from './practice-request.component';

describe('PracticeRequestComponent', () => {
  let component: PracticeRequestComponent;
  let fixture: ComponentFixture<PracticeRequestComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PracticeRequestComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PracticeRequestComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
