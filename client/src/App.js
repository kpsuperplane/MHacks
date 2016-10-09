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
      person: 0,
      loading: false
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
  complete(){
    var instance = this;
    instance.setState({appState: 0, loading: false});
    setTimeout(function(){
      instance.refs.input.focus();
    }, 100);
  }
  submit(person){
    this.setState({appState: 1, loading: true});
    var instance = this;
    this.playText(person, this.state.input, {
    onplay: function(){
      instance.setState({appState: 2, loading: false});
    },
    onfinish: instance.complete.bind(instance)});
  }
  submitLucky(){
    var instance = this;
    instance.setState({appState: 1});
    var person = 0;
    function playNext(){
      instance.setState({loading: true});
      person = (person + 1) % 3;
      var name = ["hillary", "trump", "obama"][person];
      request.get("/generate/phrase?person="+name).end(function(err, res){
        var text = res.text;
        instance.playText(name, text, {
          onplay: function(){
            instance.setState({appState: 3, input: text, person: person, loading: false});
          },
          onfinish: playNext});
      });
    }
    playNext();
  }
  videoPlayed(){
    var makeActive = this.setState.bind(this, {active: true});
    const {refs} = this;
    setTimeout(function(){
      makeActive();
      refs.input.focus();
    }, 1000);
  }
  type(e){
    this.setState({input: e.target.value});
  }
  render() {
    return (
      <div className="app">
        <div id="banner">
          <video src={boat} autoPlay={true} onPlay={this.videoPlayed.bind(this)} loop="loop"/>
          <div id="banner-inner" className={this.state.active?"active":""}>
            <div id="banner-inner-inner" className={(this.state.appState===0)?"typing":""}>
              <h1>HilarityTrumpton</h1>
              <div id="typing-container">
                {(this.state.appState===3)?(<div id="stage">
                  <img src={clinton} style={this.state.person===0?{opacity:1}:null} alt="Clinton" />
                  <img src={trump} style={this.state.person===1?{opacity:1}:null} alt="Trump" />
                  <img src={obama} style={this.state.person===2?{opacity:1}:null} alt="Obama" />
                </div>):null}
                {(this.state.appState===0)?(<input type="text" value={this.state.input} onChange={this.type.bind(this)} ref="input" placeholder="Type Right Here and Make Me Great Again &trade;"/>):(<div id="display-text">{this.state.input}</div>)}
              </div>
              <div id="button-container">
                <div className={(this.state.appState===0)?"container-section show":"container-section"}>
                  <div className={this.state.input?"hider":"hider hidden"}><button onClick={this.submit.bind(this, "hillary")}>Clinton</button><button onClick={this.submit.bind(this, "trump")}>Trump</button><button onClick={this.submit.bind(this, "obama")}>Obama</button></div><button onClick={this.submitLucky.bind(this)}>I'm Feeling Lucky</button>
                </div>
                <div className={(this.state.loading)?"container-section show":"container-section"}><img src={loading} alt="Loading"/></div>
                <div style={{marginTop:"-1em"}} className={(this.state.appState>1 && !this.state.loading)?"container-section show":"container-section"}><div id="visualizer" ref="visualizer"/></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
