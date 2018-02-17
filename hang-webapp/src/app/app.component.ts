import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = {
    label : '<hang>',
    style : {'fontFamily':" 'Kaushan Script', cursive", 'color': '#E52446'}
  };

  constructor(private router:Router){}
  backHome = () => this.router.navigate(["/s"]);
}
