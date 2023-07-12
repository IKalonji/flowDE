import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { TreeNode } from 'primeng/api';

@Component({
  selector: 'app-flowde',
  templateUrl: './flowde.component.html',
  styleUrls: ['./flowde.component.css']
})
export class FlowdeComponent implements OnInit {
  @ViewChild('codeblock', {static:false}) codeblock?: ElementRef

  dataFromSelectedFile:string = "Hello";

  workspaces: TreeNode[][] = [dummyWorkspace];

  selectedFile: string = "";

  disableEditorButton = false;

  constructor() { }

  ngOnInit(): void {
    this.codeblock?.nativeElement.click()
  }

  createWorkspace(){
    console.log("Create workspace");
  }

  nodeExpand(event:any){
    console.log("EXPAND Event: ", event);
    console.log(this.selectedFile);
  }
  
  nodeSelect(event:any){
    console.log("SELECT Event: ", event);
    console.log(this.selectedFile);
  }

  updateFile(event:any){
    console.log(event)
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
            label: 'dummyContract.cdc',
            data: 'Dummy Contract',
            icon: 'pi pi-fw pi-file',
        }
      ]
    },
    {
      key: '2',
      label: 'Transactions',
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
        key: '3',
        label: 'Tests',
        data: 'Tests Folder',
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
]
