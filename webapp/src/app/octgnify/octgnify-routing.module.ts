import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {OctgnifyComponent} from "./octgnify/octgnify.component";
import {RouterModule, Routes} from "@angular/router";

const routes: Routes = [
  {path: '', component: OctgnifyComponent}

]

@NgModule({
  declarations: [],
  imports: [
    CommonModule, RouterModule.forChild(routes)
  ]
})
export class OctgnifyRoutingModule {
}
