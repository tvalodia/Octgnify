import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OctgnifyComponent } from './octgnify.component';

describe('OctgnifyComponent', () => {
  let component: OctgnifyComponent;
  let fixture: ComponentFixture<OctgnifyComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OctgnifyComponent]
    });
    fixture = TestBed.createComponent(OctgnifyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
