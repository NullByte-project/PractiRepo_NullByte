import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListPracticesComponent } from './list-practices.component';

describe('ListPracticesComponent', () => {
  let component: ListPracticesComponent;
  let fixture: ComponentFixture<ListPracticesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ListPracticesComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ListPracticesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
