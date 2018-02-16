import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-game-page',
  templateUrl: './game-page.component.html',
  styleUrls: ['./game-page.component.css']
})
export class GamePageComponent implements OnInit {

  game : Game = new Game(); // <=== make this into object

  constructor() { }

  ngOnInit() {
    this.game.word = "3D HUBS";
    this.game.attempts = 0;
    setTimeout(()=>this.game.attempts = 1, 1000);
    setTimeout(()=>this.game.attempts = 2, 2000);
    setTimeout(()=>this.game.attempts = 3, 3000);
    setTimeout(()=>this.game.attempts = 4, 4000);
    setTimeout(()=>{this.game.attempts = 5; this.game.word="GAME OVER";}, 5000);
  }

  typedKey(key:string){
    console.log(`USER CHOSE ${key}`)
  }

}

class Game{
  attempts : number;
  word : string;
}