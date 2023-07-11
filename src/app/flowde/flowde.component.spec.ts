import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FlowdeComponent } from './flowde.component';

describe('FlowdeComponent', () => {
  let component: FlowdeComponent;
  let fixture: ComponentFixture<FlowdeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FlowdeComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FlowdeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
