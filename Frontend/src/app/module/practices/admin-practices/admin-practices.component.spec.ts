import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminPracticesComponent } from './admin-practices.component';

describe('AdminPracticesComponent', () => {
  let component: AdminPracticesComponent;
  let fixture: ComponentFixture<AdminPracticesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AdminPracticesComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AdminPracticesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
