import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {OctgnifyComponent} from './octgnify/octgnify.component';
import {OctgnifyRoutingModule} from './octgnify-routing.module';
import {MatButtonModule} from "@angular/material/button";
import {MatIconModule} from "@angular/material/icon";
import {MatInputModule} from "@angular/material/input";
import {TextFieldModule} from "@angular/cdk/text-field";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatCardModule} from "@angular/material/card";
import {FormsModule} from "@angular/forms";


@NgModule({
  declarations: [
    OctgnifyComponent
  ],
  imports: [
    CommonModule,
    OctgnifyRoutingModule,
    MatFormFieldModule,
    MatButtonModule,
    MatIconModule,
    MatInputModule,
    TextFieldModule,
    MatCardModule,
    FormsModule
  ],
  exports: [
    MatFormFieldModule,
    MatButtonModule,
    MatIconModule,
    MatInputModule,
    TextFieldModule,
  ]
})
export class OctgnifyModule {
}
