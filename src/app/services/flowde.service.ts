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

  createAccount(user: string|undefined, workspace: string|undefined, account_name:string, network: string){
    let url = this.BASE_URL + "create_account";
    let body = {
      "user": user,
      "workspace": workspace,
      "account_name": account_name,
      "network": network
    };
    return this.http.post(url, body);
  }

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

  saveToFile(user: string|undefined, workspace: string|undefined, folder:string|undefined, file:string|undefined, content:string){
    let url = this.BASE_URL + "add_to_file";
    let body = {
      "user": user,
      "workspace": workspace,
      "folder": folder,
      "file": file,
      "contents": content
    }
    return this.http.post(url, body);
  }
  
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
  
  runTransaction(user: string|undefined, workspace: string|undefined, network: string, file: string|undefined, account:string){
    let url = this.BASE_URL + "run_transaction";
    let body = {
      "user": user,
      "workspace": workspace,
      "network": network,
      "file": file,
      "account": account
    }
    return this.http.post(url, body);
  }

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
