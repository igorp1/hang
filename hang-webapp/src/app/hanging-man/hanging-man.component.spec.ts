import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HangingManComponent } from './hanging-man.component';

describe('HangingManComponent', () => {
  let component: HangingManComponent;
  let fixture: ComponentFixture<HangingManComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HangingManComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HangingManComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
