import { Injectable } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/of';
import 'rxjs/add/operator/map';

@Injectable()
export class GameApiService {

  gameID : number;
  gameCode : string;
  attempts : Array<string>;
  wordDisplay : string;

  _wordLength : number;
  set wordLength(value : number){ 
    this._wordLength = value; 
    this.wordDisplay = Array(value).fill('_').join('');
  };

  loading : boolean = false;
  errorFlag : boolean = false;

  API_base : string = "http://localhost:5000";

  constructor() { }

  newGame() : Observable<string>{
    this.wordLength = 6;
    this.gameCode = 'sjn9mS';
    return Observable.of(this.gameCode);
  }

  setupWithCode( code : string ){
    if(this.gameCode){ return; }
    this.loading = true;
    this.loadGame().subscribe(
      (d)=>{
        this.attempts = d.attempts;
        this.wordLength = d.wordLength;
        Object.keys(d.foundChars).forEach(
          (key:string)=>this.updateWord(key, d.foundChars[key]) 
        );
        this.loading = false;
      }
    );
  }

  loadGame() : Observable<any> {
    return Observable.of({
      attempts : [],
      wordLength : 6,
      foundChars : {'3': [0], 'H':[2]}
    });
  }

  checkGuess(guess : string){
     this.fetchGuessPositions(guess).subscribe(
      (pos)=>this.updateWord(guess,pos) 
     );
  }

  updateWord(character: string, positions : Array<number>){

    positions.forEach((index)=>{
      let orginalWordDisplay = this.wordDisplay;
      this.wordDisplay = orginalWordDisplay.substring(0,index);
      this.wordDisplay += character;
      this.wordDisplay += orginalWordDisplay.substring(index+1);
    });

  }

  fetchGuessPositions(guess : string) : Observable< Array<number> >{
    return Observable.of([0]);
  }

}
