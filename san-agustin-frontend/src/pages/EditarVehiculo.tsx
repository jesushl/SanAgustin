import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';
import { Estacionamiento } from '../types';

const EditarVehiculo: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [estacionamiento, setEstacionamiento] = useState<Estacionamiento | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Formulario
  const [placa, setPlaca] = useState('');
  const [modelo, setModelo] = useState('');
  const [color, setColor] = useState('');

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }

    cargarDatosVehiculo();
  }, [user, navigate]);

  const cargarDatosVehiculo = async () => {
    try {
      setLoading(true);
      const response = await apiService.getPanelResidente();
      
      if (response.error) {
        setError(response.error);
      } else if (response.data?.estacionamiento) {
        const est = response.data.estacionamiento;
        setEstacionamiento(est);
        setPlaca(est.placa || '');
        setModelo(est.modelo_auto || '');
        setColor(est.color_auto || '');
      } else {
        setError('No se encontró información del vehículo');
      }
    } catch (err) {
      setError('Error al cargar los datos del vehículo');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!estacionamiento) {
      setError('No hay vehículo para actualizar');
      return;
    }

    try {
      setSubmitting(true);
      setError(null);

      const response = await apiService.actualizarEstacionamiento(estacionamiento.id, {
        placa: placa.trim() || undefined,
        modelo_auto: modelo.trim() || undefined,
        color_auto: color.trim() || undefined
      });

      if (response.error) {
        setError(response.error);
      } else {
        setSuccess('Datos del vehículo actualizados exitosamente');
        // Actualizar el estado local
        if (response.data) {
          setEstacionamiento(response.data);
        }
      }
    } catch (err) {
      setError('Error al actualizar los datos del vehículo');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error && !estacionamiento) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Error</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => navigate('/panel-residente')}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Volver al Panel
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="px-4 py-6 sm:px-0">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Editar Datos del Vehículo
              </h1>
              <p className="mt-1 text-sm text-gray-600">
                Actualiza la información de tu vehículo registrado
              </p>
            </div>
            <button
              onClick={() => navigate('/panel-residente')}
              className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
            >
              Volver al Panel
            </button>
          </div>
        </div>

        {/* Formulario */}
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            {error && (
              <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            {success && (
              <div className="mb-4 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
                {success}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Información del Estacionamiento */}
              <div className="bg-gray-50 p-4 rounded-md">
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Información del Estacionamiento
                </h3>
                <p className="text-sm text-gray-600">
                  Número: <span className="font-medium">{estacionamiento?.numero}</span>
                </p>
              </div>

              {/* Placa */}
              <div>
                <label htmlFor="placa" className="block text-sm font-medium text-gray-700">
                  Placa del Vehículo
                </label>
                <input
                  type="text"
                  id="placa"
                  value={placa}
                  onChange={(e) => setPlaca(e.target.value)}
                  placeholder="Ej: ABC123"
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
                <p className="mt-1 text-sm text-gray-500">
                  Deja vacío si no deseas registrar una placa
                </p>
              </div>

              {/* Modelo */}
              <div>
                <label htmlFor="modelo" className="block text-sm font-medium text-gray-700">
                  Modelo del Vehículo
                </label>
                <input
                  type="text"
                  id="modelo"
                  value={modelo}
                  onChange={(e) => setModelo(e.target.value)}
                  placeholder="Ej: Toyota Corolla"
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
                <p className="mt-1 text-sm text-gray-500">
                  Deja vacío si no deseas registrar el modelo
                </p>
              </div>

              {/* Color */}
              <div>
                <label htmlFor="color" className="block text-sm font-medium text-gray-700">
                  Color del Vehículo
                </label>
                <input
                  type="text"
                  id="color"
                  value={color}
                  onChange={(e) => setColor(e.target.value)}
                  placeholder="Ej: Blanco"
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
                <p className="mt-1 text-sm text-gray-500">
                  Deja vacío si no deseas registrar el color
                </p>
              </div>

              {/* Botones */}
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => navigate('/panel-residente')}
                  className="bg-gray-300 text-gray-700 px-4 py-2 rounded-md text-sm font-medium hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className={`px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${
                    submitting
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'
                  }`}
                >
                  {submitting ? 'Actualizando...' : 'Actualizar Datos'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EditarVehiculo;
