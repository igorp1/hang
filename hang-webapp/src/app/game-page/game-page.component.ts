import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { GameApiService } from '../_services/game-api.service';

@Component({
  selector: 'app-game-page',
  templateUrl: './game-page.component.html',
  styleUrls: ['./game-page.component.css']
})
export class GamePageComponent implements OnInit {

  showMakeChallengeModal : boolean;
  showReadyChallengeModal : boolean;
  challengeModalConfig : any = {};

  // FOR DEVS
  JSON : JSON = JSON;
  viewDebugger :  boolean = false;

  constructor(private route : ActivatedRoute, private router : Router, private _game : GameApiService) {
    route.params.subscribe( (d) => this._game.setupWithCode(d.code) );
  }

  ngOnInit() { }

  typedKey(key:string){
    this._game.checkGuess(key);
  }

  newGame(){
    this._game.newGame().subscribe(
      (code) => this.router.navigate(["/game", code])
    );
  }
  
  makeChallenge(){
    this.showMakeChallengeModal = true;
  }
  
  makeChallengeLink(word){
    this._game.makeChallenge(word)
        .subscribe(
          (code) => this.showChallengeLink(code),
          (err) => this.showChallengeLink("", err)
        );
  }
  
  showChallengeLink(gameCode, issue:Response=null){
    let pathArr = location.pathname.split('/');
    pathArr.pop();
    pathArr.push(gameCode);
    let newPath = pathArr.join("/");
    let newLink = location.origin + newPath;

    if(!issue){
      this.challengeModalConfig = {
        title:'Share the link below', 
        cancelButtonLabel:'Thanks!', 
        link:newLink
      };
    }
    else{
      this.challengeModalConfig = {
        title:issue.text(),
        cancelButtonLabel:'Ok!'
      }
    }
    
    this.showReadyChallengeModal = true;
  }

}