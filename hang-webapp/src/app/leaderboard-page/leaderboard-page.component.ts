import { Component, OnInit } from '@angular/core';
import { GameApiService } from '../_services/game-api.service';

@Component({
  selector: 'app-leaderboard-page',
  templateUrl: './leaderboard-page.component.html',
  styleUrls: ['./leaderboard-page.component.css']
})
export class LeaderboardPageComponent implements OnInit {

  scores : Array<any> = [];
  errorFlag : boolean;
  loading : boolean;

  constructor(private _game : GameApiService) { }

  ngOnInit() {
    this.loadScores()
  }

  loadScores(){
    this.loading = true;
    this._game.loadTopScores().subscribe(
      (d)=>{this.scores = d;this.loading=false;},
      (err)=>{this.errorFlag=true;}
    )
  }

  getLeaderboardIndexLabel(index:number){
    let n = index+1;
    let top3 = { 1:"🥇", 2:"🥈", 3:"🥉" };
    if(n in top3) return top3[n];
    else return `${n} `;
  }
  


}
