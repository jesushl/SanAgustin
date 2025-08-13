import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';
import { PanelResidente as PanelResidenteType } from '../types';

const PanelResidente: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [panelData, setPanelData] = useState<PanelResidenteType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }

    cargarPanelResidente();
  }, [user, navigate]);

  const cargarPanelResidente = async () => {
    try {
      setLoading(true);
      const response = await apiService.getPanelResidente();
      
      if (response.error) {
        setError(response.error);
      } else if (response.data) {
        setPanelData(response.data);
      }
    } catch (err) {
      setError('Error al cargar el panel de residente');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Error</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={cargarPanelResidente}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  if (!panelData) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="px-4 py-6 sm:px-0">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Panel de Residente
              </h1>
              <p className="mt-1 text-sm text-gray-600">
                Bienvenido, {user?.email}
              </p>
            </div>
            <button
              onClick={handleLogout}
              className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
            >
              Cerrar Sesión
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Información del Departamento */}
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                Información del Departamento
              </h3>
              <div className="space-y-3">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Número de Departamento</dt>
                  <dd className="mt-1 text-sm text-gray-900">{panelData.departamento.numero}</dd>
                </div>
              </div>
            </div>
          </div>

          {/* Información del Vehículo */}
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg leading-6 font-medium text-gray-900">
                  Información del Vehículo
                </h3>
                {panelData.estacionamiento && (
                  <button
                    onClick={() => navigate('/editar-vehiculo')}
                    className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                  >
                    Editar
                  </button>
                )}
              </div>
              {panelData.estacionamiento ? (
                <div className="space-y-3">
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Número de Estacionamiento</dt>
                    <dd className="mt-1 text-sm text-gray-900">{panelData.estacionamiento.numero}</dd>
                  </div>
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Placa</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {panelData.estacionamiento.placa || 'No registrada'}
                    </dd>
                  </div>
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Modelo</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {panelData.estacionamiento.modelo_auto || 'No registrado'}
                    </dd>
                  </div>
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Color</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {panelData.estacionamiento.color_auto || 'No registrado'}
                    </dd>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-gray-500">No hay vehículo registrado</p>
              )}
            </div>
          </div>

          {/* Estado de Adeudos */}
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                Estado de Adeudos
              </h3>
              <div className="space-y-3">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Total de Adeudos</dt>
                  <dd className={`mt-1 text-2xl font-bold ${
                    panelData.total_adeudos > 0 ? 'text-red-600' : 'text-green-600'
                  }`}>
                    ${panelData.total_adeudos.toFixed(2)}
                  </dd>
                </div>
                {panelData.adeudos_pendientes.length > 0 && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Adeudos Pendientes</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {panelData.adeudos_pendientes.length} adeudo(s)
                    </dd>
                  </div>
                )}
                <div>
                  <dt className="text-sm font-medium text-gray-500">Estado de Reservas</dt>
                  <dd className={`mt-1 text-sm font-medium ${
                    panelData.puede_reservar ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {panelData.puede_reservar ? 'Puede realizar reservas' : 'No puede realizar reservas'}
                  </dd>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Menú de Opciones */}
        <div className="mt-8 bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-6">
              Servicios Disponibles
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Reserva de Área Común */}
              <div className="border border-gray-200 rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="text-lg font-medium text-gray-900">Reservar Área Común</h4>
                  {!panelData.puede_reservar && (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                      Bloqueado
                    </span>
                  )}
                </div>
                <p className="text-sm text-gray-600 mb-4">
                  Reserva espacios como la palapa, roof garden, sala de eventos, etc.
                </p>
                <button
                  onClick={() => navigate('/reserva-area-comun')}
                  disabled={!panelData.puede_reservar}
                  className={`w-full px-4 py-2 rounded-md text-sm font-medium ${
                    panelData.puede_reservar
                      ? 'bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  Reservar Área Común
                </button>
              </div>

              {/* Reserva de Lugar de Visita */}
              <div className="border border-gray-200 rounded-lg p-6">
                <h4 className="text-lg font-medium text-gray-900 mb-4">Reservar Lugar de Visita</h4>
                <p className="text-sm text-gray-600 mb-4">
                  Reserva un lugar para visitas con duración máxima de 24 horas.
                </p>
                <button
                  onClick={() => navigate('/reserva-visita')}
                  className="w-full px-4 py-2 bg-green-600 text-white rounded-md text-sm font-medium hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                >
                  Reservar Lugar de Visita
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PanelResidente;
