import React, { Component } from 'react';
import './App.css';
import boat from './boat.mp4';
import loading from './loading.svg';
import sample from './young.mp3';
import clinton from './clinton.png';
import trump from './trump.png';
import obama from './obama.png';
import request from 'superagent';
import * as q from 'q';
import {soundManager} from 'soundmanager2';
console.log(soundManager);
soundManager.setup({
  url: process.env.PUBLIC_URL + '/swf',
  useHTML5Audio: false,
  flashVersion: 9
})
class App extends Component {
  constructor(props){
    super(props);
    this.state = {
      active: false,
      appState: 0,
      input: "",
      person: 0
    }
    var instance = this;
    soundManager.onready(function(){
      var lastCheck = (new Date().getTime());
      instance.sound = soundManager.createSound({
        autoPlay: false,
        volume: 100,
        usePeakData: true,
        whileplaying: function(){
          if(instance.state.appState > 1){
            var now = (new Date().getTime());
            if(now - lastCheck < 75) return;
            lastCheck = now;
            var peak = -Math.pow((Math.max(this.peakData.left, this.peakData.right) - 1), 2) + 1;
            instance.refs.visualizer.style.transform = "scale("+peak+")";
          }
        }
      })
    })
  }
  playText(person, text, options = {}){
    var lastCheck = (new Date().getTime());
    var instance = this;
    return soundManager.createSound(Object.assign({
      url: "/generate/audio?person="+person+"&text="+encodeURIComponent(text),
      autoPlay: true,
      volume: 100,
      usePeakData: true,
      stream: true,
      whileplaying: function(){
        if(instance.state.appState > 1){
          var now = (new Date().getTime());
          if(now - lastCheck < 75) return;
          lastCheck = now;
          var peak = -Math.pow((Math.max(this.peakData.left, this.peakData.right) - 1), 2) + 1;
          instance.refs.visualizer.style.transform = "scale("+peak+")";
        }
      }
    }, options));
  }
  submit(){
    this.setState({appState: 1});
    var instance = this;
    this.playText("hillary", this.state.input, {
    onplay: function(){
      instance.setState({appState: 2});
    },
    onfinish: function(){
      instance.setState({appState: 0, input: ""});
      setTimeout(function(){
        instance.refs.input.focus();
      }, 100);
    }});
  }
  submitLucky(){
    this.setState({appState: 3, input: '', person: 1});
    refs.input.focus();
  }
  videoPlayed(){
    var makeActive = this.setState.bind(this, {active: true});
    const {refs} = this;
    setTimeout(function(){
      makeActive();
      refs.input.focus();
    }, 2000);
  }
  handleInputKeyPress(e){
    if (e.key === 'Enter') {
      this.submit();
    }
  }
  type(e){
    this.setState({input: e.target.value});
  }
  render() {
    return (
      <div className="app">
        <div id="banner">
          <video src={boat} autoPlay={true} onPlay={this.videoPlayed.bind(this)} loop={true}/>
          <div id="banner-inner" className={this.state.active?"active":""}>
            <div id="banner-inner-inner" className={(this.state.appState===0)?"typing":""}>
              <h1>ObashleyTrumpison</h1>
              <div id="typing-container">
                {(this.state.appState===3)?(<div id="stage">
                  <img src={clinton} style={this.state.person===0?{opacity:1}:null} alt="Clinton" />
                  <img src={trump} style={this.state.person===1?{opacity:1}:null} alt="Trump" />
                  <img src={obama} style={this.state.person===2?{opacity:1}:null} alt="Obama" />
                </div>):null}
                {(this.state.appState===0)?(<input type="text" value={this.state.input} onKeyPress={this.handleInputKeyPress.bind(this)} onChange={this.type.bind(this)} ref="input" placeholder="Type Right Here and Make Me Great Again &trade;"/>):this.state.input}
              </div>
              <div id="button-container">
                <div className={(this.state.appState===0)?"container-section show":"container-section"}>
                  <div className={this.state.input?"hider":"hider hidden"}><button onClick={this.submit.bind(this)}>Make My Own</button></div><button onClick={this.submitLucky.bind(this)}>I'm Feeling Lucky</button>
                </div>
                <div className={(this.state.appState===1)?"container-section show":"container-section"}><img src={loading} alt="Loading"/></div>
                <div style={{marginTop:"-2em"}} className={(this.state.appState>1)?"container-section show":"container-section"}><div id="visualizer" ref="visualizer"/></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
