import React from 'react';
import WakewordUpload from './components/wakewordUpload';
import CommandUpload from './components/commandUpload';

const App = () => (
  <div>
    <h1>Upload a Wake Word</h1>
    <WakewordUpload />
    <h1>Upload a Recording to Detect your Wake Word</h1>
    <CommandUpload />
  </div>
);

export default App;