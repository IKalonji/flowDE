import { AfterViewInit, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { TreeNode } from 'primeng/api';
import { WalletService } from '../services/wallet.service';
import { FlowdeService } from '../services/flowde.service';
import { Router } from '@angular/router';
import * as ace from "ace-builds";

@Component({
  selector: 'app-flowde',
  templateUrl: './flowde.component.html',
  styleUrls: ['./flowde.component.css']
})
export class FlowdeComponent implements OnInit, AfterViewInit {
  @ViewChild("editor") private editor: ElementRef<HTMLElement>;

  instructions:string = "Welcome to flowDE\nTo begin create a new workspace, which is a project that will contain the folders needed to begin developing on flow.";
  workspaces: TreeNode[][] = [];
  selectedFile: TreeNode = {};

  output: string = "Output displayed here!"

  setupDialogVisible = true;
  dialogMsg: string = "";

  createOrDeleteWorkspaceDialogVisible = false;
  createOrDeleteWorkspaceDialogHeader = "Manage Workspace";
  createOrDeleteWorkspaceDialogInput = "";
  createOrDeleteWorkspaceDialogLoading = false;

  fileManagement = false;
  filename = ""
  folder = {name:""}
  folders = [
    { name: 'contracts'},
    { name: 'scripts'},
    { name: ' transactions'},
    { name: 'tests'},
];
  currentManagementSelection = "";

  contractFunctions = false;
  contractFunctionSelection = "";
  account_name = "";
  network = {name:""}
  networks = [
    { name: 'emulator'},
    { name: 'testnet'},
    { name: ' mainnet'},
];

  createAccountLoading = false;
  createAccountDialogVisible = false;
  newAccountWorkspace = "";

  aceEditor: any;

  executionOutputDialog = false;
  executionLoading = true;
  executionOutput = "";

  constructor(private walletService: WalletService, private flowdeService: FlowdeService, private router: Router) {}

  ngOnInit(): void {
      this.dialogMsg = "Checking if user exists using the wallet used to sign in"
      this.flowdeService.isUser(this.walletService.wallet).subscribe((user:any)=>{
        console.log("response from isuser", user);
        if(user.result == "OK"){
          this.dialogMsg = "User is valid. Getting your workspaces"
          this.flowdeService.getWorkspaces(this.walletService.wallet).subscribe((workspace:any)=>{
            console.log(workspace);
            this.buildWorkspaceTreeObject(workspace.data)
            this.dialogMsg = "";
            this.setupDialogVisible = false;
          })
        }
        else { 
          this.dialogMsg = "User not found. Creating a user with wallet used to sign in"
          this.flowdeService.createUser(this.walletService.wallet).subscribe((newUser: any)=>{
            console.log(newUser)
            this.dialogMsg = "User created";
            this.setupDialogVisible = false;
          })
        }
      });
  }

  ngAfterViewInit(): void {
    ace.config.set("fontSize", "14px");
    this.aceEditor = ace.edit(this.editor.nativeElement);
    this.aceEditor.session.setValue(this.instructions);
  }
  
  nodeExpand(event:any){
    console.log("EXPAND Event: ", event);
    console.log(this.selectedFile);
    this.aceEditor.setValue(this.selectedFile.data);
  }
  
  nodeSelect(event:any){
    console.log("SELECT Event: ", event);
    console.log("SELECTED FILE: ", this.selectedFile);
    this.aceEditor.setValue(this.selectedFile.data);
  }

  workspace(){
    console.log("setup dialog for manage");
    this.createOrDeleteWorkspaceDialogVisible = true;
  }

  getWorkspace(){
    this.flowdeService.getWorkspaces(this.walletService.wallet).subscribe((workspace:any)=>{
      console.log(workspace);
      if(workspace.result == "OK"){
        this.buildWorkspaceTreeObject(workspace.data)
      }
    })
  }

  createWorkspace(){
    this.createOrDeleteWorkspaceDialogLoading = true;
    console.log("executing create");
    this.showExecutionOutput()
          this.flowdeService.createWorkspace(this.walletService.wallet, this.createOrDeleteWorkspaceDialogInput).subscribe(
            (data: any)=>{
              console.log(data.result);
              this.createOrDeleteWorkspaceDialogLoading = false;
              this.createOrDeleteWorkspaceDialogVisible = false;
              this.getWorkspace();
              this.executionOutput = `Result:${data.result} -- Detail:${data.detail} --Error:${data.error ? data.error : "None"}`
              this.executionLoading = false
            }
          )
  }

  deleteWorkspace(){
    this.createOrDeleteWorkspaceDialogLoading = true;
    console.log("executing delete");
    this.showExecutionOutput()
          this.flowdeService.deleteWorkspace(this.walletService.wallet, this.createOrDeleteWorkspaceDialogInput).subscribe(
            (data: any)=>{
              console.log(data.result);
              this.createOrDeleteWorkspaceDialogLoading = false;
              this.createOrDeleteWorkspaceDialogVisible = false;
              this.getWorkspace();
              this.executionOutput = `Result:${data.result} -- Detail:${data.detail} --Error:${data.error ? data.error : "None"}`
              this.executionLoading = false
            }
          )
  }

  addAccount(){
    console.log("Add account to flow.json");
    this.createAccountDialogVisible = true;
  }

  createAccount(){
    this.createAccountLoading = !this.createAccountLoading
    this.showExecutionOutput()
    this.flowdeService.createAccount(this.walletService.wallet, this.newAccountWorkspace, this.account_name, this.network.name).subscribe(
      (data: any) => {
        this.executionOutput = `Result:${data.result} -- Detail:${data.detail} --Error:${data.error ? data.error : "None"} -- Data:${data.data}`
        this.getWorkspace();
        this.createAccountLoading = false;
        this.createAccountDialogVisible = false;
        this.newAccountWorkspace = "";
        this.executionLoading = false
      }
    )
  }

  logout(){
    console.log("Logout");
    this.walletService.disconnect()
    this.router.navigate([""]);
  }

  fileOptions(action: string){
    this.fileManagement = !this.fileManagement;
    this.currentManagementSelection = action;
  }

  saveFile(){
    console.log("Save file");
    let valueFromText = this.aceEditor.getValue()
    console.log(valueFromText);
    this.showExecutionOutput()
    this.flowdeService.saveToFile(this.walletService.wallet, this.selectedFile.parent?.type, this.selectedFile.parent?.label?.toLowerCase(), this.selectedFile.label, valueFromText).subscribe(
      (data:any)=>{
        this.executionOutput = `Result:${data.result} -- Detail:${data.detail} --Error:${data.error ? data.error : "None"}`
        this.executionLoading = false
      }
    )
  }

  newFile(workspace:string | undefined){
    console.log("New File");  
    this.showExecutionOutput()  
    this.flowdeService.createFile(this.walletService.wallet, workspace, this.folder.name, this.filename).subscribe(
      (data:any)=>{
        this.executionOutput = `Result:${data.result} -- Detail:${data.detail} --Error:${data.error ? data.error : "None"}`
        this.getWorkspace();
        this.fileManagement = false;
        this.executionLoading = false
      }
    )
  }

  deleteFile(workspace: string | undefined){
    console.log("Delete File");
    this.showExecutionOutput()
    this.flowdeService.deleteFile(this.walletService.wallet, workspace, this.folder.name, this.filename).subscribe(
      (data:any)=>{
        this.executionOutput = `Result:${data.result} -- Detail:${data.detail} --Error:${data.error ? data.error : "None"}`
        this.getWorkspace();
        this.fileManagement = false;
        this.executionLoading = false
      }
    )
  }

  contractOptions(action: string){
    this.contractFunctions = !this.contractFunctions;
    this.contractFunctionSelection = action;
  }

  deployContract(){
    console.log("Deploy Contract");
    this.showExecutionOutput()
    if(this.selectedFile.parent?.label == "Contracts" && this.selectedFile.label?.endsWith(".cdc")){
      this.flowdeService.deployContract(this.walletService.wallet, this.selectedFile.parent.type, this.account_name, this.network.name, this.selectedFile.label).subscribe(
        (data:any)=>{
          this.executionOutput = `Result:${data.result} -- Detail:${data.detail} --Error:${data.error ? data.error : "None"}`
          this.resetContractFunctionVariables()
          this.executionLoading = false
        }
      )
    }
    else {
      this.executionOutput = `Result: ERROR -- Detail: SELECT A CONTRACT FILE BY CLICKING ON IT --Error: NO CONTRACT SELECTED`
      this.resetContractFunctionVariables()
      this.executionLoading = false
    }
  }

  runScript(){
    console.log("Run Script");
    this.showExecutionOutput()
    if(this.selectedFile.parent?.label == "Scripts" && this.selectedFile.label?.endsWith(".cdc")){
      this.flowdeService.runScript(this.walletService.wallet, this.selectedFile.parent.type, this.network.name, this.selectedFile.label).subscribe(
        (data:any)=>{
          this.executionOutput = `Result:${data.result} -- Detail:${data.detail} --Error:${data.error ? data.error : "None"}`
          this.executionLoading = false
          this.resetContractFunctionVariables()
        }
      )
    }
    else{
      this.executionOutput = `Result: ERROR -- Detail: SELECT A SCRIPT FILE BY CLICKING ON IT --Error: NO SCRIPT SELECTED`
      this.executionLoading = false
      this.resetContractFunctionVariables()
    }
  }

  runTransaction(){
    console.log("Run Transaction");
    this.showExecutionOutput()
    if(this.selectedFile.parent?.label == "Transactions" && this.selectedFile.label?.endsWith(".cdc")){
      this.flowdeService.runTransaction(this.walletService.wallet, this.selectedFile.parent.type, this.network.name, this.selectedFile.label, this.account_name).subscribe(
        (data:any)=>{
          this.executionOutput = `Result:${data.result} -- Detail:${data.detail} --Error:${data.error ? data.error : "None"}`
          this.executionLoading = false
          this.resetContractFunctionVariables()
        }
      )
    }
    else{
      this.executionOutput = `Result: ERROR -- Detail: SELECT A TRANSACTION FILE BY CLICKING ON IT --Error: NO TRANSACTION SELECTED`
      this.executionLoading = false;
      this.resetContractFunctionVariables()
    }
  }

  buildWorkspaceTreeObject(workspaceResponse: any[]){
    this.workspaces = []
    if(workspaceResponse.length == 0) return;
    workspaceResponse.forEach(_workspace => {
    const _contracts: any[] = _workspace.folders.contracts;
    const _scripts: any[] = _workspace.folders.scripts;
    const _transactions: any[] = _workspace.folders.transactions;
    const _tests: any[] = _workspace.folders.tests; 

    let contractsTreenode: TreeNode = {
      type: _workspace.workspace,
      label: "Contracts",
      data: 'Contracts Folder',
      icon: 'pi pi-fw pi-folder-open',
      children: []
      }
    
    let scriptsTreenode: TreeNode = {
      type: _workspace.workspace,
      label: "Scripts",
      data: 'Scripts Folder',
      icon: 'pi pi-fw pi-folder-open',
      children: []
      }
    let transactionsTreenode: TreeNode = {
      type: _workspace.workspace,
      label: "Transactions",
      data: 'Transactions Folder',
      icon: 'pi pi-fw pi-folder-open',
      children: []
      }
    let testsTreenode: TreeNode = {
      type: _workspace.workspace,
      label: "Tests",
      data: 'Tests Folder',
      icon: 'pi pi-fw pi-folder-open',
      children: []
      }
    let flowJSONTreenode: TreeNode = {
      type: _workspace.workspace,
      label: "flow.json",
      data: `${_workspace['flow.json']}`,
      icon: 'pi pi-fw pi-file',
      }
    let readmeTreenode: TreeNode = {
      type: _workspace.workspace,
      label: "README.md",
      data: `${_workspace['README.md']}`,
      icon: 'pi pi-fw pi-file',
      }
    
    _contracts.forEach((_element: any) => {
      let newChild: TreeNode = {
        label: _element.name,
        data: `${_element.content}`,
        icon: 'pi pi-fw pi-file',
      }
      contractsTreenode.children?.push(newChild)
    });
    _scripts.forEach((_element: any) => {
      let newChild: TreeNode = {
        label: _element.name,
        data: `${_element.content}`,
        icon: 'pi pi-fw pi-file',
      }
      scriptsTreenode.children?.push(newChild)
    });
    _transactions.forEach((_element: any) => {
      let newChild: TreeNode = {
        label: _element.name,
        data: `${_element.content}`,
        icon: 'pi pi-fw pi-file',
      }
      transactionsTreenode.children?.push(newChild)
    });
    _tests.forEach((_element: any) => {
      let newChild: TreeNode = {
        label: _element.name,
        data: `${_element.content}`,
        icon: 'pi pi-fw pi-file',
      }
      testsTreenode.children?.push(newChild)
    });
    let _workspaceTreeNode:TreeNode[] = [contractsTreenode, scriptsTreenode, transactionsTreenode, testsTreenode, flowJSONTreenode, readmeTreenode]; 
    this.workspaces.push(_workspaceTreeNode);
    });
  }

  resetContractFunctionVariables(){
    this.contractFunctions = false;
    this.contractFunctionSelection = "";
    this.account_name = "";
    this.network = {name:""}
  }

  showExecutionOutput(){
    this.executionOutputDialog = true;
  }

  closeExecutionOutput(){
    this.executionOutputDialog = false;
    this.executionLoading = true;
    this.executionOutput = "";
  }
}
