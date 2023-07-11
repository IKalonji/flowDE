import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { WalletService } from '../services/wallet.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private router: Router, private walletService: WalletService) { }

  ngOnInit(): void {
  }

  gotoIDE(){
    this.walletService.connect().then((data)=>{
      if(this.walletService.connected) this.router.navigate(["flowde"]);
    })
    
  }

}
