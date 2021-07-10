import React from 'react';
import './App.css';
import NavigationBar from './Components/NavigationBar/NavigationBar';

function App() {
  require('dotenv').config()

  return (
    <div className="App">
      <NavigationBar />
    </div>
  );
}


export default App;
