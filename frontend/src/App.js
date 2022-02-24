import React from 'react';
import Recorder from './components/recorder';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      currentWakeword: null,
    };
  }

  //set callback to hold wakeword
  setWakeword = (wakeword) => {
    this.setState({currentWakeword: wakeword});
  }

  render() {
    return (
      <div>        
        <h1>~~~ Wake Word Detection ~~~</h1>
        <h3>by <a href="https://www.linkedin.com/in/csalexiuk/">Chris</a>, <a href="https://www.linkedin.com/in/sinasinai/">Sina</a>, and <a href="https://www.linkedin.com/in/max-calabro-47531b2/">Max</a></h3>        
        <img src="turtle.png" alt="turtle" width="85" height="100"></img><img src="turtle.png" alt="turtle" width="85" height="100"></img><img src="turtle.png" alt="turtle" width="85" height="100"></img>
          <Recorder/>
          <br></br>
          <br></br>
          <br></br>
        <i>This is an implementation of <a href="https://arxiv.org/abs/2006.11477">Wav2Vec2</a></i>
      </div>
      
    ); 
  }
}

export default App;