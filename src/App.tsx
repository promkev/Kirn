import React from 'react';
import './App.css';
import LoginButton from './Components/LoginButton/LoginButton';
function App() {
  require('dotenv').config()

  return (
    <div className="App">
      <header className="App-header">
        <LoginButton />
      </header>
    </div>
  );
}


export default App;
