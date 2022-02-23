import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faStar } from '@fortawesome/free-solid-svg-icons'
import { faStar as farStar } from '@fortawesome/free-regular-svg-icons'

class WakewordUpload extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      wakeword: '',
      success: false,
      wakewordStrength: 100,
    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  strengthColor(strength) {
    if (strength >= 21) {
      return 'red';
    }
    else if (strength >= 11) {
      return 'orange';
    }
    else if (strength >= 6) {
      return 'yellow';
    }
    else if (strength >= 3) {
      return 'yellow-green';
    }
    return 'green';
  }

  handleUploadImage(ev) {
    ev.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);

    fetch('http://127.0.0.1:5000/api/wakeword', {
      method: 'POST',
      body: data,
    }).then((response) => {
      response.json().then((body) => {
        this.props.setwakeword(body.wakeword);
        this.setState({ success: body.success });
        this.setState({ wakeword: body.wakeword });
        this.setState({ wakewordStrength: body.wakewordStrength });
        console.log(this.state.wakewordStrength);
      });
    });
  }

  render() {
    if (this.state.success) {
      return (
        <form onSubmit={this.handleUploadImage}>
          <div>
            <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
          </div>
          <br />
          <div>
            <button>Upload</button>
          </div>
          <div style={{flex: 1, color: this.state.success ? this.strengthColor(this.state.wakewordStrength) : 'red'}}>
            <br></br>
            <h1>Wakeword / Strength</h1>
            <p>We understood your wake word to be: {this.state.wakeword}</p>
            <p>Out of 5 stars, we rate your wakeword:</p>
            <FontAwesomeIcon icon={ this.state.wakewordStrength < 21  ? faStar : farStar}/>
            <FontAwesomeIcon icon={ this.state.wakewordStrength < 11  ? faStar : farStar}/>
            <FontAwesomeIcon icon={ this.state.wakewordStrength < 6  ? faStar : farStar}/>
            <FontAwesomeIcon icon={ this.state.wakewordStrength < 3  ? faStar : farStar} />
            <FontAwesomeIcon icon={ this.state.wakewordStrength < 2  ? faStar : farStar} />
          </div>
        </form>
      );
    }
    return (
      <form onSubmit={this.handleUploadImage}>
          <div>
            <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
          </div>
          <br />
          <div>
            <button>Upload</button>
          </div>
        </form>
    );
  }
}

export default WakewordUpload;