import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {RouterModule, Routes} from "@angular/router";


const routes: Routes = [
  {
    path: '',
    loadChildren: () => import('./octgnify/octgnify.module').then(m => m.OctgnifyModule)
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes)
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
