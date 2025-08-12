import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Estacionamientos from './pages/Estacionamientos';

// Páginas placeholder para las demás secciones
const Contactos: React.FC = () => (
  <div className="min-h-screen bg-gray-50 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">Contactos</h1>
      <p className="text-gray-600">Página en desarrollo</p>
    </div>
  </div>
);

const Reservas: React.FC = () => (
  <div className="min-h-screen bg-gray-50 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">Reservas</h1>
      <p className="text-gray-600">Página en desarrollo</p>
    </div>
  </div>
);

const Adeudos: React.FC = () => (
  <div className="min-h-screen bg-gray-50 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">Adeudos</h1>
      <p className="text-gray-600">Página en desarrollo</p>
    </div>
  </div>
);

const QR: React.FC = () => (
  <div className="min-h-screen bg-gray-50 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">Generador de QR</h1>
      <p className="text-gray-600">Página en desarrollo</p>
    </div>
  </div>
);

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/estacionamientos" element={<Estacionamientos />} />
          <Route path="/contactos" element={<Contactos />} />
          <Route path="/reservas" element={<Reservas />} />
          <Route path="/adeudos" element={<Adeudos />} />
          <Route path="/qr" element={<QR />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
