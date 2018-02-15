import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit {

  greeting : String = "Hello";
  greetings : Array<String> = [
    "Ready to play some hangman?",
    "Welcome!",
    "Wanna <hang>"
  ];

  constructor(private router: Router) { }

  ngOnInit() {
    this.greeting = this.greetings[Math.floor(Math.random() * this.greetings.length)];
  }

  newGame() {
    let gameCode = "cRbw76"
    this.router.navigate(["/game", gameCode]);
  }

  openLeaderboard(){
    this.router.navigate(["/top10"]);
  }
  

}
