import { Component, OnInit, Input } from '@angular/core';
import 'rxjs/add/operator/map';
import * as THREE from 'three';

@Component({
  selector: 'word-display',
  templateUrl: './word-display.component.html',
  styleUrls: ['./word-display.component.css']
})
export class WordDisplayComponent implements OnInit {

  _word : string;
  @Input() set word(value : string){
    this._word = value;
    if(this.hasInitialized){ this.updateText(); }
  }

  // control vars
  wasClicked : boolean = false;
  hasInitialized : boolean = false;
  showClickHelpImage : boolean = false;

  // THREE objects
  canvasContainer : HTMLElement;
  font: THREE.font;
  textMesh : THREE.Mesh;
  cameraTarget : THREE.Vector3;
  camera : THREE.PerspectiveCamera;
  scene : THREE.Scene = new THREE.Scene();
  group : THREE.Group = new THREE.Group();
  renderer : THREE.WebGLRenderer = new THREE.WebGLRenderer();
  
  // rotation vars
  mouseX : number = 0;
  targetRotation : number = 0;
  mouseXOnMouseDown : number = 0;
  targetRotationOnMouseDown : number= 0;

  constructor() { }

  ngOnInit() {
    this.loadCanvasContainer();
    this.initThreeObjects();
    this.animate();
    setTimeout(()=>{
      this.showClickHelpImage = true;
      setTimeout(()=>{this.showClickHelpImage = false;}, 2000)
    }, 3000);
  }

  // INIT
  loadCanvasContainer(){ 
    this.canvasContainer = document.getElementById("canvas-conatiner")
    this.addRotationListeners()
  }

  initThreeObjects(){
    // CAMERA
    this.camera = new THREE.PerspectiveCamera( 30, window.innerWidth / window.innerHeight, 1, 1500 );
    this.camera.position.set( 0, 400, 700 );
    this.camera.aspect = this.getCameraAspectRatio();
    this.cameraTarget = new THREE.Vector3( 0, 150, 0 );
    this.camera.updateProjectionMatrix();

    // SCENE
    //this.scene.background = new THREE.Color( 0x000000 );
    var dirLight = new THREE.DirectionalLight( 0xffffff, 0.125 );
    dirLight.position.set( 0, 0, 1 ).normalize();
    this.scene.add( dirLight );

    var pointLight = new THREE.PointLight( 0xffffff, 1.5 );
    pointLight.position.set( 0, 100, 90 );
    this.scene.add( pointLight );

    // GROUP
    this.group.position.y = 100;
    this.scene.add(this.group);

    // RENDERER
    this.renderer = new THREE.WebGLRenderer({antialias: true, alpha: true});
    this.renderer.setSize( ...this.getRendererSize() );
    this.renderer.setPixelRatio(window.devicePixelRatio);
    this.canvasContainer.appendChild( this.renderer.domElement );

    // WINDOW RESIZE
    window.addEventListener('resize', ()=>{ 
      this.camera.aspect = this.getCameraAspectRatio();
      this.camera.updateProjectionMatrix();
      this.renderer.setSize( ...this.getRendererSize() ); 
    });

    // LOAD FONT
    var loader = new THREE.FontLoader();
    loader.load("/assets/fonts/Raleway.json",(font)=>{
      this.font = font;
      this.updateText();
      this.hasInitialized = true;
    })

  }

  // TEXT 
  updateText(){
    this.group.remove(this.textMesh);
    this.buildText(this._word);
  }

  buildText(TEXT : string){
    let geometrySettings = {
      font: this.font,
      size: 80,
      height: 20,
      curveSegments: 4,
      bevelThickness: 2,
      bevelSize: 1.5,
      bevelEnabled: 1,
      material: 0,
      extrudeMaterial: 1
    };
    let textGeometry = new THREE.TextGeometry( TEXT , geometrySettings);
    textGeometry.computeBoundingBox();
    textGeometry.computeVertexNormals();
    var centerOffset = -0.5 * ( textGeometry.boundingBox.max.x - textGeometry.boundingBox.min.x );

    this.textMesh = new THREE.Mesh( textGeometry, [new THREE.MeshNormalMaterial(), new THREE.MeshNormalMaterial()] );

    this.textMesh.position.x = centerOffset;
    this.textMesh.position.y = 30;
    this.textMesh.position.z = 0;

    this.textMesh.rotation.x = 0;
    this.textMesh.rotation.y = Math.PI * 2;

    this.group.add( this.textMesh );
    
  }

  // CONTAINER HELPERS
  getCameraAspectRatio() : number{
    return this.canvasContainer.offsetWidth/this.canvasContainer.offsetHeight;
  }

  getRendererSize() : Array<number>{
    return [this.canvasContainer.offsetWidth, this.canvasContainer.offsetHeight];
  }
  
  // ROTATION
  addRotationListeners(){

    this.canvasContainer.addEventListener('mousedown', (event) =>{
      event.preventDefault();
      this.wasClicked = true;
      this.addMouseListeners();
      this.mouseXOnMouseDown = event.clientX - this.getRendererSize()[0];
      this.targetRotationOnMouseDown = this.targetRotation;
    });
    this.canvasContainer.addEventListener('touchstart', (event) =>{
      if (event.touches.length == 1) {
        event.preventDefault();
        this.mouseXOnMouseDown = event.touches[0].pageX - this.getRendererSize()[0];
        this.targetRotationOnMouseDown = this.targetRotation;
      }
    });
    this.canvasContainer.addEventListener('touchmove', (event) =>{
      if (event.touches.length == 1) {
        event.preventDefault();
        this.mouseX = event.touches[0].pageX - this.getRendererSize()[0];
        this.targetRotation = this.targetRotationOnMouseDown + (this.mouseX - this.mouseXOnMouseDown) * 0.05;
      }
    });

  }

  onMouseMove = (e) => {
    this.mouseX = e.clientX - this.getRendererSize()[0]/2;
    this.targetRotation = this.targetRotationOnMouseDown + (this.mouseX - this.mouseXOnMouseDown) * 0.02;
  }

  addMouseListeners = ()=>{
    this.canvasContainer.addEventListener('mousemove', this.onMouseMove);
    this.canvasContainer.addEventListener('mouseup', this.removeMouseListeners);
    this.canvasContainer.addEventListener('mouseout', this.removeMouseListeners);
  }

  removeMouseListeners = ()=>{
    document.removeEventListener('mousemove', this.onMouseMove);
    document.removeEventListener('mouseup', this.removeMouseListeners);
    document.removeEventListener('mouseout', this.removeMouseListeners);
  }

  // ANIMATE ~~0o0~~
  render(){ 
    this.group.rotation.y += ( this.targetRotation - this.group.rotation.y ) * 0.05;
    this.camera.lookAt(this.cameraTarget);
    this.renderer.clear();
    this.renderer.render(this.scene, this.camera);
  }

  animate = () => { requestAnimationFrame(this.animate); this.render(); }


}
