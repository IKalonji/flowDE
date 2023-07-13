import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class FlowdeService {

  BASE_URL = environment.base_url;

  constructor(private http: HttpClient) { }

  isServiceReady(){
    return this.http.get(this.BASE_URL+"ready");
  }

  isServiceLive(){
    return this.http.get(this.BASE_URL+"live");
  }

  isUser(user:string | undefined){
    let url = this.BASE_URL+"is_user";
    let body = {
      "user": user
    }
    return this.http.post(url,body);
  }

  createUser(user:string | undefined){
    let url = this.BASE_URL+"create_user";
    let body = {
      "user": user
    }
    return this.http.post(url,body);
  }

  createAccount(){}

  getWorkspaces(user: string | undefined){
    let url = this.BASE_URL+"get_workspaces";
    let body = {
      "user": user
    }
    return this.http.post(url,body);
  }

  createWorkspace(user: string|undefined, name: string){
    let url = this.BASE_URL+"create_workspace";
    let body = {
      "user": user,
      "workspace": name
    }
    return this.http.post(url,body);
  }

  deleteWorkspace(user: string|undefined, name: string){
    let url = this.BASE_URL+"delete_workspace";
    let body = {
      "user": user,
      "workspace": name
    }
    return this.http.post(url,body);
  }

  createFile(user:string | undefined, workspace:string | undefined, folder: string, filename:string){
    let url = this.BASE_URL+"create_file";
    let body = {
      "user": user,
      "workspace": workspace,
      "folder": folder,
      "file": filename
    }
    return this.http.post(url,body);
  }

  deleteFile(user:string | undefined, workspace:string | undefined, folder: string, filename:string){
    let url = this.BASE_URL+"delete_file";
    let body = {
      "user": user,
      "workspace": workspace,
      "folder": folder,
      "file": filename
    }
    return this.http.post(url,body);
  }

  renameFile(){}
  addtoFile(){}
  
  deployContract(user: string|undefined, workspace:string|undefined, account_name: string, network: string = 'testnet', file:string){
    let url = this.BASE_URL + "deploy_contract";
    let body = {
      "user": user,
      "workspace": workspace,
      "account_name": account_name,
      "network": network,
      "file": file
    }
    return this.http.post(url, body)
  }
  runTransaction(){}
  
  runScript(user: string|undefined, workspace:string|undefined, network:string, file:string){
    let url = this.BASE_URL + "run_script";
    let body = {
      "user": user,
      "workspace": workspace,
      "network": network,
      "file": file
    }
    return this.http.post(url, body);
  }

}

/*
            "create_workspace": self.create_workspace,
            "delete_workspace": self.delete_workspace,
            "get_workspace": self.get_workspace,
            "create_file": self.create_file,
            "rename_file": self.rename_file,
            "add_to_file": self.add_to_file,
            "delete_file": self.delete_file,
            "deploy_contracts":self.deploy_contracts,
            "run_transaction":self.run_transaction,
            "run_script": self.run_script,
            "create_account": self.create_account,
            "create_user": self.create_user,
*/
