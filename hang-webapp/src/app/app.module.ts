import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { HomePageComponent } from './home-page/home-page.component';
import { GamePageComponent } from './game-page/game-page.component';
import { LeaderboardPageComponent } from './leaderboard-page/leaderboard-page.component';
import { WordDisplayComponent } from './word-display/word-display.component';
import { KeyBoardComponent } from './key-board/key-board.component';

export const ROUTES: Routes = [
  { path: '', component: HomePageComponent },
  { path: 'game/:code', component: GamePageComponent },
  { path: 'top10', component: LeaderboardPageComponent },
];

@NgModule({
  declarations: [
    AppComponent,
    HomePageComponent,
    GamePageComponent,
    LeaderboardPageComponent,
    WordDisplayComponent,
    KeyBoardComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(ROUTES)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
