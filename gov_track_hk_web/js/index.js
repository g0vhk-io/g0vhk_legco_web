import React from 'react';
import ReactDOM from 'react-dom';
import Home from './home/Home'

const container = document.getElementById('home-root');
if (container) {
  ReactDOM.render(
    <Home/>,
    container
  );
}
