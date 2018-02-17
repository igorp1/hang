import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'simple-modal',
  templateUrl: './simple-modal.component.html',
  styleUrls: ['./simple-modal.component.css']
})
export class SimpleModalComponent implements OnInit {

  @Input() show : boolean;
  @Output() showChange : EventEmitter<boolean> = new EventEmitter<boolean>();

  @Input() config : any = {};

  @Output() value : EventEmitter<string> = new EventEmitter<string>();

  input : string;

  constructor() { }

  ngOnInit() {}

  done(){
    this.value.emit(this.input);
    this.close()
  }

  cancel(){
    this.close()
  }

  close(){
    this.input = "";
    this.show = false;
    this.showChange.emit(this.show);
  }

}
