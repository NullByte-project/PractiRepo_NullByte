import { TestBed } from '@angular/core/testing';

import { ServicioLogicaService } from './servicio-logica.service';

describe('ServicioLogicaService', () => {
  let service: ServicioLogicaService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ServicioLogicaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
