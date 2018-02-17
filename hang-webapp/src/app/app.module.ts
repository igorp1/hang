import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule, Http, RequestOptions }   from '@angular/http';

import { AppComponent } from './app.component';
import { HomePageComponent } from './home-page/home-page.component';
import { GamePageComponent } from './game-page/game-page.component';
import { LeaderboardPageComponent } from './leaderboard-page/leaderboard-page.component';
import { WordDisplayComponent } from './word-display/word-display.component';
import { KeyBoardComponent } from './key-board/key-board.component';
import { HangingManComponent } from './hanging-man/hanging-man.component';
import { SimpleModalComponent } from './simple-modal/simple-modal.component';

import { GameApiService } from './_services/game-api.service';

export const ROUTES: Routes = [
  { path: '', component: HomePageComponent },
  { path: 'game/:code', component: GamePageComponent },
  { path: 'top10', component: LeaderboardPageComponent },
  { path: '**', redirectTo : '' }
];

@NgModule({
  declarations: [
    AppComponent,
    HomePageComponent,
    GamePageComponent,
    LeaderboardPageComponent,
    WordDisplayComponent,
    KeyBoardComponent,
    HangingManComponent,
    SimpleModalComponent
  ],
  imports: [
    BrowserModule,
    HttpModule,
    RouterModule.forRoot(ROUTES),
    FormsModule
  ],
  providers: [GameApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
