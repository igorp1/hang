import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { GameApiService } from '../_services/game-api.service';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss']
})
export class HomePageComponent implements OnInit {

  greeting : String;
  greetings : Array<String> = [
    "Ready to play some hangman?",
    "Welcome!",
    "Wanna <hang>"
  ];

  constructor(private router: Router, public _game : GameApiService) { }

  ngOnInit() {
    this.greeting = this.greetings[Math.floor(Math.random() * this.greetings.length)];
  }

  newGame() {
    this._game.newGame().subscribe(
      (code) => this.router.navigate(["/game", code])
    );
  }

  openLeaderboard(){
    this.router.navigate(["/top10"]);
  }

}
