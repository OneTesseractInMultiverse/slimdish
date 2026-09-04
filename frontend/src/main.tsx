import React from 'react';
import ReactDOM from 'react-dom/client';
import '@carbon/styles/css/styles.css';
import './styles.scss';
import App from './App';

const root = document.getElementById('root');
if (!root) throw new Error('Application root was not found');

ReactDOM.createRoot(root).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);

