import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import RegistrationSuccess from './pages/RegistrationSuccess';
import AdminPanel from './pages/AdminPanel';
import PanelResidente from './pages/PanelResidente';
import ReservaAreaComun from './pages/ReservaAreaComun';
import ReservaVisita from './pages/ReservaVisita';
import EditarVehiculo from './pages/EditarVehiculo';
import AuthSuccess from './pages/AuthSuccess';
import AuthError from './pages/AuthError';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/registration-success" element={<RegistrationSuccess />} />
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="/panel-residente" element={<PanelResidente />} />
          <Route path="/reserva-area-comun" element={<ReservaAreaComun />} />
          <Route path="/reserva-visita" element={<ReservaVisita />} />
          <Route path="/editar-vehiculo" element={<EditarVehiculo />} />
          <Route path="/auth-success" element={<AuthSuccess />} />
          <Route path="/auth-error" element={<AuthError />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
