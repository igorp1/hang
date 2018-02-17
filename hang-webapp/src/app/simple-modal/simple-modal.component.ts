import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'simple-modal',
  templateUrl: './simple-modal.component.html',
  styleUrls: ['./simple-modal.component.scss']
})
export class SimpleModalComponent implements OnInit {

  @Input() show : boolean;
  @Output() showChange : EventEmitter<boolean> = new EventEmitter<boolean>();

  @Input() config : ModalConfig;

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

export class ModalConfig{
  link:string;
  title:string;
  askInput:boolean;
  okButtonLabel:string;
  inputPlaceholder:string;
  cancelButtonLabel:string;
  constructor(initializer:any){
    for(let key of Object.keys(initializer)){
      try{ this[key] = initializer[key]; }
      catch(err){ throw `The property ${key} does not belong to ModalConfig`; }
    }
  }
}