import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { GameApiService } from '../_services/game-api.service';

@Component({
  selector: 'app-game-page',
  templateUrl: './game-page.component.html',
  styleUrls: ['./game-page.component.css']
})
export class GamePageComponent implements OnInit {

  JSON : JSON = JSON;
  viewDebugger :  boolean = false;

  constructor(private route : ActivatedRoute, private _game : GameApiService) {
    route.params.subscribe( (d) => this._game.setupWithCode(d.code) );
  }

  ngOnInit() { }

  typedKey(key:string){
    this._game.checkGuess(key);
  }

  newGame(){

  }

  

}