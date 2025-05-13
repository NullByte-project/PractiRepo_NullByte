import { TestBed } from '@angular/core/testing';

import { NotificaconesService } from './notificacones.service';

describe('NotificaconesService', () => {
  let service: NotificaconesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NotificaconesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
