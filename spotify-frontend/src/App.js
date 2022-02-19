import React from 'react';
import WakewordUpload from './components/wakewordUpload';
import CommandUpload from './components/commandUpload';

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
        <h1>Upload a Wake Word</h1>
          <WakewordUpload setwakeword={this.setWakeword}/>
        <h1>Upload a Recording to Detect your Wake Word</h1>
          <CommandUpload wakeword={this.state.currentWakeword}/>
      </div>
    ); 
  }
}

export default App;