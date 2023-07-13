import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { WalletService } from '../services/wallet.service';
import { FlowdeService } from '../services/flowde.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private router: Router, private walletService: WalletService, private flowdeService: FlowdeService) { }

  ngOnInit(): void {
  }

  gotoIDE(){
    this.walletService.connect().then(()=>{
      this.flowdeService.isServiceReady().subscribe((data:any)=>{
        if(data.result == "OK"){
          if(this.walletService.connected) this.router.navigate(["flowde"]);
        }
      })
    })
    
  }

}
