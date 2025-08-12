import React, { useState, useEffect } from 'react';
import { Car, Search, Plus, Eye, QrCode } from 'lucide-react';
import type { Estacionamiento } from '../types';

const Estacionamientos: React.FC = () => {
  const [estacionamientos, setEstacionamientos] = useState<Estacionamiento[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedEstacionamiento, setSelectedEstacionamiento] = useState<Estacionamiento | null>(null);
  const [showModal, setShowModal] = useState(false);

  // Formulario para nueva reserva de visita
  const [reservaForm, setReservaForm] = useState({
    numero_departamento: '',
    placas_visita: '',
    hora_llegada: '',
    horas_estancia: 2
  });

  useEffect(() => {
    // Simular datos de estacionamientos
    const mockEstacionamientos: Estacionamiento[] = [
      {
        numero_estacionamiento: 'A1',
        placa: 'ABC-123',
        modelo: 'Toyota Corolla',
        color: 'Blanco',
        es_visita: false
      },
      {
        numero_estacionamiento: 'A2',
        placa: 'XYZ-789',
        modelo: 'Honda Civic',
        color: 'Negro',
        es_visita: false
      },
      {
        numero_estacionamiento: 'V1',
        placa: 'VIS-001',
        modelo: 'Nissan Sentra',
        color: 'Gris',
        es_visita: true
      }
    ];
    setEstacionamientos(mockEstacionamientos);
  }, []);

  const filteredEstacionamientos = estacionamientos.filter(est =>
    est.numero_estacionamiento.toLowerCase().includes(searchTerm.toLowerCase()) ||
    est.placa.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleReservaVisita = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Aquí iría la llamada real a la API
      console.log('Reserva de visita:', reservaForm);
      setShowModal(false);
      setReservaForm({
        numero_departamento: '',
        placas_visita: '',
        hora_llegada: '',
        horas_estancia: 2
      });
    } catch (error) {
      console.error('Error al crear reserva:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Gestión de Estacionamientos
              </h1>
              <p className="mt-2 text-gray-600">
                Administra los estacionamientos y registra visitas
              </p>
            </div>
            <button
              onClick={() => setShowModal(true)}
              className="btn-primary flex items-center"
            >
              <Plus className="w-4 h-4 mr-2" />
              Registrar Visita
            </button>
          </div>
        </div>

        {/* Search Bar */}
        <div className="mb-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Buscar por número de estacionamiento o placa..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field pl-10"
            />
          </div>
        </div>

        {/* Estacionamientos Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredEstacionamientos.map((estacionamiento) => (
            <div key={estacionamiento.numero_estacionamiento} className="card">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <div className={`p-2 rounded-lg ${estacionamiento.es_visita ? 'bg-orange-100' : 'bg-blue-100'}`}>
                    <Car className={`w-5 h-5 ${estacionamiento.es_visita ? 'text-orange-600' : 'text-blue-600'}`} />
                  </div>
                  <div className="ml-3">
                    <h3 className="font-semibold text-gray-900">
                      Estacionamiento {estacionamiento.numero_estacionamiento}
                    </h3>
                    <span className={`text-sm px-2 py-1 rounded-full ${
                      estacionamiento.es_visita 
                        ? 'bg-orange-100 text-orange-800' 
                        : 'bg-blue-100 text-blue-800'
                    }`}>
                      {estacionamiento.es_visita ? 'Visita' : 'Residente'}
                    </span>
                  </div>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Placa:</span>
                  <span className="text-sm font-medium">{estacionamiento.placa}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Modelo:</span>
                  <span className="text-sm font-medium">{estacionamiento.modelo}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Color:</span>
                  <span className="text-sm font-medium">{estacionamiento.color}</span>
                </div>
              </div>

              <div className="mt-4 flex space-x-2">
                <button
                  onClick={() => setSelectedEstacionamiento(estacionamiento)}
                  className="btn-secondary flex-1 flex items-center justify-center text-sm"
                >
                  <Eye className="w-4 h-4 mr-1" />
                  Ver Detalles
                </button>
                <button className="btn-primary flex-1 flex items-center justify-center text-sm">
                  <QrCode className="w-4 h-4 mr-1" />
                  QR
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Modal para registrar visita */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-md w-full p-6">
              <h2 className="text-xl font-semibold mb-4">Registrar Visita</h2>
              <form onSubmit={handleReservaVisita} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Número de Departamento
                  </label>
                  <input
                    type="text"
                    value={reservaForm.numero_departamento}
                    onChange={(e) => setReservaForm({...reservaForm, numero_departamento: e.target.value})}
                    className="input-field"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Placas del Vehículo
                  </label>
                  <input
                    type="text"
                    value={reservaForm.placas_visita}
                    onChange={(e) => setReservaForm({...reservaForm, placas_visita: e.target.value})}
                    className="input-field"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Hora de Llegada
                  </label>
                  <input
                    type="datetime-local"
                    value={reservaForm.hora_llegada}
                    onChange={(e) => setReservaForm({...reservaForm, hora_llegada: e.target.value})}
                    className="input-field"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Horas de Estancia
                  </label>
                  <select
                    value={reservaForm.horas_estancia}
                    onChange={(e) => setReservaForm({...reservaForm, horas_estancia: parseInt(e.target.value)})}
                    className="input-field"
                  >
                    <option value={1}>1 hora</option>
                    <option value={2}>2 horas</option>
                    <option value={4}>4 horas</option>
                    <option value={8}>8 horas</option>
                  </select>
                </div>
                <div className="flex space-x-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="btn-secondary flex-1"
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    disabled={loading}
                    className="btn-primary flex-1"
                  >
                    {loading ? 'Registrando...' : 'Registrar'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Modal de detalles */}
        {selectedEstacionamiento && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-md w-full p-6">
              <h2 className="text-xl font-semibold mb-4">
                Detalles del Estacionamiento
              </h2>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Número:</span>
                  <span className="text-sm font-medium">{selectedEstacionamiento.numero_estacionamiento}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Placa:</span>
                  <span className="text-sm font-medium">{selectedEstacionamiento.placa}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Modelo:</span>
                  <span className="text-sm font-medium">{selectedEstacionamiento.modelo}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Color:</span>
                  <span className="text-sm font-medium">{selectedEstacionamiento.color}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Tipo:</span>
                  <span className={`text-sm px-2 py-1 rounded-full ${
                    selectedEstacionamiento.es_visita 
                      ? 'bg-orange-100 text-orange-800' 
                      : 'bg-blue-100 text-blue-800'
                  }`}>
                    {selectedEstacionamiento.es_visita ? 'Visita' : 'Residente'}
                  </span>
                </div>
              </div>
              <div className="mt-6 flex space-x-3">
                <button
                  onClick={() => setSelectedEstacionamiento(null)}
                  className="btn-secondary flex-1"
                >
                  Cerrar
                </button>
                <button className="btn-primary flex-1">
                  Generar QR
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Estacionamientos;
