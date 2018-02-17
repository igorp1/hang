import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'hanging-man',
  templateUrl: './hanging-man.component.html',
  styleUrls: ['./hanging-man.component.scss']
})
export class HangingManComponent implements OnInit {

  @Input() width : string = "60px";
  @Input() height : string = "60px";

  @Input() attempts : number;

  constructor() { }

  ngOnInit() { 
    if(this.attempts === undefined){
      throw "HangingManComponent requires 'attempts' value to be passed to directive before it's initialized";
    }
  }

}
