import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Estacionamientos from './pages/Estacionamientos';
import Login from './pages/Login';
import Register from './pages/Register';
import RegistrationSuccess from './pages/RegistrationSuccess';
import AdminPanel from './pages/AdminPanel';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/estacionamientos" element={<Estacionamientos />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/registration-success" element={<RegistrationSuccess />} />
          <Route path="/admin" element={<AdminPanel />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
