import React from 'react';

class WakewordUpload extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      wakeword: '',
      success: false,
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
        this.setState({ wakeword: body.transcript });
        this.setState({ success: body.success });
      });
    });
  }

  render() {
    return (
      <form onSubmit={this.handleUploadImage}>
        <div>
          <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
        </div>
        <br />
        <div>
          <button>Upload</button>
        </div>
        <p style={{ color: this.state.success ? 'green' : 'red'}}>{this.state.wakeword}</p>
      </form>
    );
  }
}

export default WakewordUpload;