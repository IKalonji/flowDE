import { TestBed } from '@angular/core/testing';

import { FlowdeService } from './flowde.service';

describe('FlowdeService', () => {
  let service: FlowdeService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FlowdeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
