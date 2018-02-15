import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
@Component({
  selector: 'keyboard',
  templateUrl: './key-board.component.html',
  styleUrls: ['./key-board.component.css']
})
export class KeyBoardComponent implements OnInit {

  characterSetup: Array< Array<string> >;
  @Input()
  keyLogger:Array<string> = [];
  @Output() 
  readKey: EventEmitter<String> = new EventEmitter();


  constructor() { }

  ngOnInit() { 
    this.setKeyboardSetup('QWERT');
  }

  setKeyboardSetup(setupName : string){
    let characterOrders = {
      'QWERT' : [ '.1234567890'.split(''),
                  '.QWERTYUIOP'.split(''),
                  '..ASDFGHJKL'.split(''),
                  '._.ZXCVBNM'.split('')
                ],
      'ABC'   : [ '1234567890'.split(''),
                  'ABCDEFGHIJ'.split(''),
                  '_KLMNOPQRS'.split(''),
                  '__TUVWXYZ'.split('')
                ]
    };
    this.characterSetup = characterOrders[setupName];
  }

  clickedOn(key, emmitClick=true){
    this.keyLogger.push(key)
    if(emmitClick){
      this.readKey.emit(key);
    }
  }

}
