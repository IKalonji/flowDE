import { Injectable } from '@angular/core';
import * as fcl from "@onflow/fcl";

@Injectable({
  providedIn: 'root'
})
export class WalletService {

  connected: boolean | undefined;
  wallet: string | undefined;

  constructor() {
    fcl.config({
      "discovery.wallet": "https://fcl-discovery.onflow.org/testnet/authn", // Endpoint set to Testnet
      'accessNode.api': 'https://rest-testnet.onflow.org',
      "app.detail.title": "flowDE",
      "app.detail.icon": "https://github.com/IKalonji/flowDE/blob/main/src/assets/flow-logo.png",
    })
  }

  async connect(){
    await fcl.authenticate().then(async ()=>{
      this.connected = true; 
      await fcl.currentUser.snapshot().then((data)=>{
        console.log(data);
        this.wallet = data.addr;
        this.connected = data.loggedIn;
      })
    }).catch((error)=>{
      alert(error);
    })
  }

  async disconnect(){
    fcl.unauthenticate();
    this.connected = false;
    this.wallet = "";
  }


}
