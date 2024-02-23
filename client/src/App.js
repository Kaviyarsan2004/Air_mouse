import React, { useState } from 'react';
import './App.css';
import point from './/point.jpg';
import click from './/click.jpg';
import scrup from './/scrup.jpg';
import srldown from './/srldown.jpg';

const App = () => {
  const [isStreaming, setIsStreaming] = useState(true);
  const [enableDraw, setEnableDraw] = useState(false);

  const streamSrc = isStreaming ? 'http://127.0.0.1:5000/video_feed' : '';

  const handleToggleStreaming = () => {
    setIsStreaming(!isStreaming);
  };

  const handleToggleDrawFun = async () => {
    setEnableDraw(!enableDraw);
  
    if (!enableDraw) { // If enabling draw, start speech to text
      try {
        await fetch('http://127.0.0.1:5000/start_speech_to_text', { method: 'POST' });
        console.log('Speech to text started');
      } catch (error) {
        console.error('Error starting speech to text:', error);
      }
    } else { // If disabling draw, stop speech to text
      try {
        await fetch('http://127.0.0.1:5000/stop_speech_to_text', { method: 'POST' });
        console.log('Speech to text stopped');
      } catch (error) {
        console.error('Error stopping speech to text:', error);
      }
    }
  };

  return (
    <div className="app">
      <header className="header">AirMouse</header>

      <div className="main-container">
        <div className="video-and-controls">
          <div className="video-container">
            {isStreaming ? (
              <img src={streamSrc} alt="Video Feed" style={{ width: '100%', height: 'auto' }} />
            ) : (
              <div className="video-placeholder">Stream Paused</div>
            )}
          </div>
        </div>

        <div className="control-section">
          <button onClick={handleToggleStreaming} className={isStreaming ? 'pause' : 'resume'}>
                {isStreaming ? 'Pause' : 'Resume'}
          </button>
          <label className="switch" id="switch">
            <input type="checkbox" checked={enableDraw} onChange={handleToggleDrawFun} />
            <span className="slider round"></span>
          </label>
          <h1>AirMouse</h1>
          <p>It is a HID designed to work by tracking your finger and based on hand gestures.</p>
          <div id="box"> 
            <h2>Move:</h2>
            <img src={point}></img>
          </div>
          <div id="box"> 
            <h2>Click:</h2>
            <img src={click}></img>
          </div>
          <div id="box"> 
            <h2>Scroll up:</h2>
            <img src={scrup}></img>
          </div>
          <div id="box"> 
            <h2>Scroll down:</h2>
            <img src={srldown}></img>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
