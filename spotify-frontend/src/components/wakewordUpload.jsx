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

  handleUploadImage(ev) {
    ev.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);

    fetch('http://localhost:5000/api/wakeword', {
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
          <div style={{flex: 1, flexDirection: 'row'}}>
            <p style={{ color: this.state.success ? 'green' : 'red'}}>{this.state.wakeword}</p>
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