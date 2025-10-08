// Ponto de entrada da aplicação ReactJS
// Renderiza o componente App no DOM
// Configuração básica do React 18

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
