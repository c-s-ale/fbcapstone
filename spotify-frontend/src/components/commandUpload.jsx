import React from 'react';
import './command.css';

class CommandUpload extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      transcript: '',
      success: false,
    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  handleUploadImage(ev) {
    ev.preventDefault();

    const data = new FormData();
    const wakeword = this.props.wakeword;
    data.append('wakeword', wakeword);
    data.append('file', this.uploadInput.files[0]);
    

    fetch('http://localhost:5000/api/command', {
      method: 'POST',
      body: data,
    }).then((response) => {
      response.json().then((body) => {
        this.setState({ transcript: body.transcript });
        this.setState({ success: body.success });
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
        {this.state.set = true}
        <p>After parsing the audio you submitted we detected your wakeword and parsed the following command: </p>
        <p style={{ color: this.state.success ? 'light-green' : 'red'}}>{this.state.transcript}</p>
      </form>
    );
  } else {
    return (
    <form onSubmit={this.handleUploadImage}>
        <div>
          <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
        </div>
        <br />
        <div>
          <button>Upload</button>
        </div>
        <p>Either you have not submitted audio, or we could not detect your wakeword.</p>
      </form>
    );
    }
  }
}

export default CommandUpload;