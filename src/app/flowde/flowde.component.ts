import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { TreeNode } from 'primeng/api';

@Component({
  selector: 'app-flowde',
  templateUrl: './flowde.component.html',
  styleUrls: ['./flowde.component.css']
})
export class FlowdeComponent implements OnInit {

  dataFromSelectedFile:string = "Welcome to flowDE\nTo begin create a new workspace, which is a project that will contain the folders needed to begin developing on flow.";

  workspaces: TreeNode[][] = [dummyWorkspace];

  selectedFile: TreeNode = {};

  disableEditorButton = false;

  output: string = "Output displayed here!"

  constructor() {}

  ngOnInit(): void {
  }

  createWorkspace(){
    console.log("Create workspace");
  }

  nodeExpand(event:any){
    console.log("EXPAND Event: ", event);
    console.log(this.selectedFile);
    this.dataFromSelectedFile = this.selectedFile?.data;
  }
  
  nodeSelect(event:any){
    console.log("SELECT Event: ", event);
    console.log("SELECTED FILE: ", this.selectedFile);
    this.dataFromSelectedFile = this.selectedFile?.data;
  }

  saveFile(event:any){
    console.log(event)
    console.log("Save file");
    this.selectedFile.data = this.dataFromSelectedFile;
    console.log(this.selectedFile?.data);
  }

  newWorkspace(){
    console.log("New workspace");
  }

  logout(){
    console.log("Logout");
  }
}

export const dummyWorkspace = [
  {
    key: '0',
    label: 'Contracts',
    data: 'Contracts Folder',
    icon: 'pi pi-fw pi-inbox',
    children: [
        {
            key: '0-0',
            label: 'dummyContract.cdc',
            data: 'Dummy Contract',
            icon: 'pi pi-fw pi-file',
        }
      ]
  },
  {
    key: '1',
    label: 'Scripts',
    data: 'Scripts Folder',
    icon: 'pi pi-fw pi-inbox',
    children: [
        {
            key: '0-0',
            label: 'scripts.cdc',
            data: 'Dummy Scripts',
            icon: 'pi pi-fw pi-file',
        }
      ]
    },
  {
    key: '2',
    label: 'Transactions',
    data: 'transactions Folder',
    icon: 'pi pi-fw pi-inbox',
    children: [
      {
          key: '0-0',
          label: 'transactions.cdc',
          data: 'Dummy transaction',
          icon: 'pi pi-fw pi-file',
      }
    ]
  },
  {
    key: '3',
    label: 'Tests',
    data: 'Tests Folder',
    icon: 'pi pi-fw pi-inbox',
    children: [
      {
          key: '0-0',
          label: 'testfile.cdc',
          data: 'Dummy Test',
          icon: 'pi pi-fw pi-file',
      }
    ]
  },
  {
    key: '4',
    label: 'flow.json',
    data: 'flow.json content',
    icon: 'pi pi-fw pi-inbox',
  },

]
