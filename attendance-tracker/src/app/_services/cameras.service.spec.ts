import { TestBed } from '@angular/core/testing';

import { CamerasService } from './cameras.service';

describe('CamerasService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: CamerasService = TestBed.get(CamerasService);
    expect(service).toBeTruthy();
  });
});
