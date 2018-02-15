import { Component, OnInit, Input } from '@angular/core';
import * as THREE from 'three';

@Component({
  selector: 'word-display',
  templateUrl: './word-display.component.html',
  styleUrls: ['./word-display.component.css']
})
export class WordDisplayComponent implements OnInit {

  @Input() word : String;
  canvasContainer : HTMLElement;

  // 3D objects
  scene : THREE.Scene = new THREE.Scene();
  renderer : THREE.WebGLRenderer = new THREE.WebGLRenderer();
  camera : THREE.PerspectiveCamera;

  constructor() { }

  ngOnInit() {
    this.loadCanvasContainer();
    this.buildScene();
    let renderThis = this.addTestCube();
    this.render();
  }

  render(){
    this.renderer.render(this.scene, this.camera);
  }

  addTestCube(){
    var geometry = new THREE.BoxGeometry(20, 20, 20);
    var material = new THREE.MeshLambertMaterial({color: 0xfd59d7});
    var cube = new THREE.Mesh(geometry, material);
    this.scene.add(cube);

    /* we need to add a light so we can see our cube - its almost
    as if we're turning on a lightbulb within the room */
    var light = new THREE.PointLight(0xFFFF00);
    /* position the light so it shines on the cube (x, y, z) */
    light.position.set(10, 0, 25);
    this.scene.add(light);
  }

  loadCanvasContainer(){ 
    this.canvasContainer = document.getElementById("canvas-conatiner") 
  }

  getCameraAspectRatio() : number{
    return this.canvasContainer.offsetWidth/this.canvasContainer.offsetHeight;
  }

  getRendererSize() : Array<number>{
    return [this.canvasContainer.offsetWidth, this.canvasContainer.offsetHeight];
  }

  buildScene(){

    // add a camera
    // THREE.PerspectiveCamera(fov, aspect, near, far)
    this.camera = new THREE.PerspectiveCamera( 75, this.getCameraAspectRatio(),  0.1,  1000 );
    this.camera.position.z = 100;

    // add a renderer
    this.renderer = new THREE.WebGLRenderer();
    this.renderer.setSize( ...this.getRendererSize() );
    
    //setup window resize adjust
    window.addEventListener('resize', ()=>{ 
      this.renderer.setSize( ...this.getRendererSize() ); 
      this.camera.aspect = this.getCameraAspectRatio();
    });

    // ADD RENDERER TO PAGE ~ovo~
    this.canvasContainer.appendChild( this.renderer.domElement );

  }

}
