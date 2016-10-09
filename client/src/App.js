import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import boat from './boat.mp4';
import loading from './loading.svg';

class App extends Component {
  constructor(props){
    super(props);
    this.state = {
      active: false,
      appState: 0,
      input: ""
    }
  }
  submit(){
    this.setState({appState: 1});
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
            <div id="banner-inner-inner" className={(this.state.appState==0)?"typing":""}>
              <h1>ObashleyTrumpison</h1>
              <div id="typing-container">
                {(this.state.appState==0)?(<input type="text" value={this.state.input} onKeyPress={this.handleInputKeyPress.bind(this)} onChange={this.type.bind(this)} ref="input" placeholder="Type Right Here and Make Me Great Again &trade;"/>):this.state.input}
              </div>
              <div id="button-container">
                <div className={(this.state.appState==0)?"container-section show":"container-section"}>
                  <div className={this.state.input?"hider":"hider hidden"}><button onClick={this.submit.bind(this)}>Make My Own</button></div><button onClick={this.submit.bind(this)}>I'm Feeling Lucky</button>
                </div>
                <div className={(this.state.appState==1)?"container-section show":"container-section"}><img src={loading} /></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
