import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';
import { AreaComun, ReservaAreaComun } from '../types';

const ReservaAreaComun: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [areasComunes, setAreasComunes] = useState<AreaComun[]>([]);
  const [reservasExistentes, setReservasExistentes] = useState<ReservaAreaComun[]>([]);
  const [selectedArea, setSelectedArea] = useState<number | ''>('');
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }

    cargarDatos();
  }, [user, navigate]);

  const cargarDatos = async () => {
    try {
      setLoading(true);
      const [areasResponse, reservasResponse] = await Promise.all([
        apiService.getAreasComunes(),
        apiService.getReservasAreaComunUsuario()
      ]);

      if (areasResponse.data) {
        setAreasComunes(areasResponse.data);
      }

      if (reservasResponse.data) {
        setReservasExistentes(reservasResponse.data);
      }
    } catch (err) {
      setError('Error al cargar los datos');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedArea || !fechaInicio || !fechaFin) {
      setError('Por favor complete todos los campos');
      return;
    }

    const inicio = new Date(fechaInicio);
    const fin = new Date(fechaFin);

    if (inicio >= fin) {
      setError('La fecha de fin debe ser posterior a la fecha de inicio');
      return;
    }

    if (inicio < new Date()) {
      setError('No puede reservar fechas pasadas');
      return;
    }

    try {
      setSubmitting(true);
      setError(null);

      const response = await apiService.crearReservaAreaComun({
        area_comun_id: selectedArea as number,
        periodo_inicio: fechaInicio,
        periodo_fin: fechaFin
      });

      if (response.error) {
        setError(response.error);
      } else {
        setSuccess('Reserva creada exitosamente');
        setSelectedArea('');
        setFechaInicio('');
        setFechaFin('');
        // Recargar reservas
        const reservasResponse = await apiService.getReservasAreaComunUsuario();
        if (reservasResponse.data) {
          setReservasExistentes(reservasResponse.data);
        }
      }
    } catch (err) {
      setError('Error al crear la reserva');
    } finally {
      setSubmitting(false);
    }
  };

  const isDateDisabled = (date: string) => {
    const selectedDate = new Date(date);
    return reservasExistentes.some(reserva => {
      const inicio = new Date(reserva.periodo_inicio);
      const fin = new Date(reserva.periodo_fin);
      return selectedDate >= inicio && selectedDate <= fin;
    });
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="px-4 py-6 sm:px-0">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Reservar Área Común
              </h1>
              <p className="mt-1 text-sm text-gray-600">
                Selecciona un área común y las fechas para tu reserva
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

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Formulario de Reserva */}
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-6">
                Nueva Reserva
              </h3>

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
                {/* Selección de Área Común */}
                <div>
                  <label htmlFor="area" className="block text-sm font-medium text-gray-700">
                    Área Común
                  </label>
                  <select
                    id="area"
                    value={selectedArea}
                    onChange={(e) => setSelectedArea(e.target.value ? parseInt(e.target.value) : '')}
                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                    required
                  >
                    <option value="">Selecciona un área</option>
                    {areasComunes.map((area) => (
                      <option key={area.id} value={area.id}>
                        {area.nombre} - {area.ubicacion}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Fecha y Hora de Inicio */}
                <div>
                  <label htmlFor="fechaInicio" className="block text-sm font-medium text-gray-700">
                    Fecha y Hora de Inicio
                  </label>
                  <input
                    type="datetime-local"
                    id="fechaInicio"
                    value={fechaInicio}
                    onChange={(e) => setFechaInicio(e.target.value)}
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    required
                  />
                </div>

                {/* Fecha y Hora de Fin */}
                <div>
                  <label htmlFor="fechaFin" className="block text-sm font-medium text-gray-700">
                    Fecha y Hora de Fin
                  </label>
                  <input
                    type="datetime-local"
                    id="fechaFin"
                    value={fechaFin}
                    onChange={(e) => setFechaFin(e.target.value)}
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    required
                  />
                </div>

                {/* Botón de Envío */}
                <button
                  type="submit"
                  disabled={submitting}
                  className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${
                    submitting
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'
                  }`}
                >
                  {submitting ? 'Creando Reserva...' : 'Crear Reserva'}
                </button>
              </form>
            </div>
          </div>

          {/* Calendario de Reservas Existentes */}
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-6">
                Mis Reservas
              </h3>

              {reservasExistentes.length === 0 ? (
                <p className="text-gray-500 text-center py-8">
                  No tienes reservas activas
                </p>
              ) : (
                <div className="space-y-4">
                  {reservasExistentes.map((reserva) => (
                    <div
                      key={reserva.id}
                      className="border border-gray-200 rounded-lg p-4"
                    >
                      <div className="flex justify-between items-start">
                        <div>
                          <h4 className="font-medium text-gray-900">
                            {reserva.area_comun.nombre}
                          </h4>
                          <p className="text-sm text-gray-600">
                            {reserva.area_comun.ubicacion}
                          </p>
                        </div>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          reserva.estado === 'activa'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {reserva.estado}
                        </span>
                      </div>
                      <div className="mt-2 text-sm text-gray-600">
                        <p><strong>Inicio:</strong> {formatDate(reserva.periodo_inicio)}</p>
                        <p><strong>Fin:</strong> {formatDate(reserva.periodo_fin)}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReservaAreaComun;
