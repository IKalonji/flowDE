import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import {StyleClassModule} from 'primeng/styleclass';
import { ButtonModule } from 'primeng/button';
import { HomeComponent } from './home/home.component';
import { FlowdeComponent } from './flowde/flowde.component';

import { SidebarModule } from 'primeng/sidebar';
import { ToolbarModule } from 'primeng/toolbar';
import { EditorModule } from 'primeng/editor';
import { SplitButtonModule } from 'primeng/splitbutton';
import { InputTextModule } from 'primeng/inputtext';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { TreeModule } from 'primeng/tree';


@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    FlowdeComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    StyleClassModule,
    BrowserAnimationsModule,
    ButtonModule,
    RouterModule,
    FormsModule,
    SidebarModule,
    ToolbarModule,
    EditorModule,
    SplitButtonModule,
    InputTextModule,
    InputTextareaModule,
    TreeModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
