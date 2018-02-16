import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
@Component({
  selector: 'keyboard',
  templateUrl: './key-board.component.html',
  styleUrls: ['./key-board.component.css']
})
export class KeyBoardComponent implements OnInit {

  characterSetup: Array< Array<string> >;
  @Input() disabled:Array<string> = [];
  @Output() disabledChange : EventEmitter<Array<string>> = new EventEmitter<Array<string>>();
  @Output() readKey: EventEmitter<String> = new EventEmitter();


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

  clickedOn(key, enabled, emmitClick=true){
    if(!enabled){return;}
    this.disabled.push(key)
    this.disabledChange.emit(this.disabled);
    if(emmitClick){
      this.readKey.emit(key);
    }
  }

}
