import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-game-page',
  templateUrl: './game-page.component.html',
  styleUrls: ['./game-page.component.css']
})
export class GamePageComponent implements OnInit {

  gameWord : string = "3D HUBS"

  constructor() { }

  ngOnInit() {
  }

  typedKey(key:string){
    console.log(`USER CHOSE ${key}`)
  }

}
