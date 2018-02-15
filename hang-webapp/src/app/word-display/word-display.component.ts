import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'word-display',
  templateUrl: './word-display.component.html',
  styleUrls: ['./word-display.component.css']
})
export class WordDisplayComponent implements OnInit {

  @Input()
  word : String;

  constructor() { }

  ngOnInit() {
  }

}
