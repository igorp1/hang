import { Injectable } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/of';
import 'rxjs/add/operator/map';

@Injectable()
export class GameApiService {

  gameID : number;
  gameCode : string;
  mistakes : number = 0;
  attempts : Array<string> = [];
  wordDisplay : string;

  _wordLength : number;
  set wordLength(value : number){ 
    this._wordLength = value; 
    this.wordDisplay = Array(value).fill('_').join('');
  };

  _status : string; // playing|won|lost
  set status(value:string){
    if(['playing','won','lost'].indexOf(value) == -1){ 
      throw "The given status is not valid" 
    }
    this._status = value;
    switch(this._status){
      case 'won':
        this.wordDisplay = "YOU WON!";
        break;
      case 'lost':
        this.wordDisplay = "GAME OVER";
    }
  }

  loading : boolean = false;
  errorFlag : boolean = false;

  API_base : string = "http://localhost:5000";

  constructor(private http : Http) { }

  cleanup(){
    this.gameID  = undefined;
    this.gameCode  = undefined;
    this.mistakes = 0;
    this.attempts  = [];
    this.wordDisplay  = undefined;
    this._wordLength = undefined;
    this._status = 'playing';
    this.loading  = false;
    this.errorFlag  = false;
  }

  newGame() : Observable<string>{
    this.loading = true;
    this.cleanup()
    return this.http.get(this.API_base + '/game/new')
      .map( (res:Response) => res.json() )
      .map( (gameInfo)=>{ 
        this.loading = false;
        this.gameCode = gameInfo.game_code;
        this.wordLength = gameInfo.word_length;
        return this.gameCode;
      },
      (err)=>this.errorHandler(err)
    );
  }

  setupWithCode( code : string ){
    if(this.gameCode){ return; }
    this.loading = true;
    this.gameCode = code;
    this.loadGame().subscribe(
      (d)=>{
        this.mistakes = d.mistakeCount;
        this.attempts = d.attempts;
        if(d.status != 'playing'){
          this.status = d.status;
        }
        else{
          this.status = 'playing';
          this.wordLength = d.wordLength;
          Object.keys(d.foundChars).forEach(
            (key:string)=>this.updateWord(key, d.foundChars[key]) 
          );
        }
        this.loading = false;
      },
      (err)=>this.errorHandler(err)
    )
    ;
  }

  loadGame() : Observable<any> {
    return this.http.get(this.API_base + `/game/${this.gameCode}/load`)
            .map( (res: Response) => res.json());
  }

  errorHandler(res:Response){
    this.loading = false;
    this.errorFlag = true;
    this.wordDisplay = res.status == 0 ? '500' : String(res.status);
  }

  checkGuess(guess : string){
    this.fetchGuessPositions(guess).subscribe(
      (guessResult)=>{
        if(!guessResult['found']){this.mistakes+=1;}
        this.updateWord(guess,guessResult['positions']);
        this.status = guessResult['status'];
      },
      (err)=>this.errorHandler(err)
    );
  }

  fetchGuessPositions(guess : string) : Observable< Array<any> >{
    return this.http.post(this.API_base + `/game/${this.gameCode}/check`,
            {'guess':guess})
            .map((res : Response)=> res.json());
  }

  updateWord(character: string, positions : Array<number>){

    positions.forEach((index)=>{
      let orginalWordDisplay = this.wordDisplay;
      this.wordDisplay = orginalWordDisplay.substring(0,index);
      this.wordDisplay += character;
      this.wordDisplay += orginalWordDisplay.substring(index+1);
    });

  }

}
