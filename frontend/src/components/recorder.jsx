import React from 'react';
import './command.css';
import AudioReactRecorder, { RecordState } from 'audio-react-recorder'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faStar } from '@fortawesome/free-solid-svg-icons'
import { faStar as farStar } from '@fortawesome/free-regular-svg-icons'


class Recorder extends React.Component {

    constructor(props) {
      super(props)
  
      this.state = {
        recordState: null,
        recordingUrl: null,
        blob: null,
        uploaded: null,
        detected: null,
        command: null,
        wakeword: null
      }
    }
  
    start = () => {
      this.setState({
        recordState: RecordState.START
      })
    }

    pause = () => {
      this.setState({
        recordState: RecordState.PAUSE
      })
    }
  
    stop = () => {
      this.setState({
        recordState: RecordState.STOP
      })
    }
  
    //audioData contains blob and blobUrl
    onStop = (audioData) => {
      //console.log('audioData', audioData)
      console.log(audioData)
      this.setState({
          recordingUrl: audioData.url,
          blob: audioData.blob
      }, () => console.log('recording blob url', this.state.recordingUrl))

    }

    play = () => {
        var audio = new Audio(this.state.recordingUrl);
        audio.play();
    }

    submitWakeword = () => {


        const data = new FormData();
        data.append('file', this.state.blob);
    
        fetch('/api/wakeword', {
        method: 'POST',
        body: data,
        }).then((response) => {
        response.json().then((body) => {            
            this.setState({ uploaded: body.success });
            this.setState({ strength: body.strength });
            this.setState({ wakeword: body.wakeword });
        });
    });
    }

    submitCommand = () => {


        const data = new FormData();
        data.append('file', this.state.blob);
        data.append('wakeword', this.state.wakeword);
    
        fetch('/api/command', {
        method: 'POST',
        body: data,
        }).then((response) => {
        response.json().then((body) => {
            this.setState({ command: body.command });
            this.setState({ detected: body.success });
        });
    });
    }
  
    render() {
      const { recordState } = this.state
  
      return (
        <div>
          <AudioReactRecorder state={recordState} onStop={this.onStop} backgroundColor={'gold'} foregroundColor={'green'}/>
          <button onClick={this.start}>Start</button>
          {' '}
          <button onClick={this.pause}>Pause</button>
          {' '}
          <button onClick={this.stop}>Stop</button>
          <p><br></br>Click "Start" to begin recording!</p>          
          <br></br>
          <button onClick={this.play}>Play Recorded Audio</button> 
          {' '}          
          <button onClick={this.submitWakeword}>Submit Wake Word</button>
          {' '}
          <button onClick={this.submitCommand}>Submit Command</button>
          <p>Your wake word is: <b>{this.state.wakeword}</b> 
          <br></br>
          <br></br>
          <p>Out of 5 stars, we rate your wakeword:</p>
            <FontAwesomeIcon icon={ this.state.strength < 21  ? faStar : farStar}/>
            <FontAwesomeIcon icon={ this.state.strength < 11  ? faStar : farStar}/>
            <FontAwesomeIcon icon={ this.state.strength < 6  ? faStar : farStar}/>
            <FontAwesomeIcon icon={ this.state.strength < 3  ? faStar : farStar} />
            <FontAwesomeIcon icon={ this.state.strength < 2  ? faStar : farStar} />
          <br></br>
          <br></br>
          Your detected command was: <b>{this.state.command}</b> 
          </p>
        </div>
      )
    }
}

export default Recorder;