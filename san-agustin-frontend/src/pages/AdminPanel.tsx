import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

interface PendingRegistration {
  id: number;
  email: string;
  nombre: string;
  apellido: string;
  provider: string;
  telefono: string;
  direccion: string;
  departamento: string;
  notas_adicionales: string;
  created_at: string;
}

const AdminPanel: React.FC = () => {
  const navigate = useNavigate();
  const [pendingRegistrations, setPendingRegistrations] = useState<PendingRegistration[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [approvingId, setApprovingId] = useState<number | null>(null);

  useEffect(() => {
    fetchPendingRegistrations();
  }, []);

  const fetchPendingRegistrations = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/login');
        return;
      }

      const response = await fetch('http://localhost:8000/auth/pending-registrations', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.status === 401) {
        localStorage.removeItem('token');
        navigate('/login');
        return;
      }

      if (response.ok) {
        const data = await response.json();
        setPendingRegistrations(data);
      } else {
        setError('Error al cargar registros pendientes');
      }
    } catch (err) {
      setError('Error de conexión');
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (registrationId: number) => {
    setApprovingId(registrationId);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/auth/approve-registration/${registrationId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        // Remover el registro aprobado de la lista
        setPendingRegistrations(prev => prev.filter(reg => reg.id !== registrationId));
        alert('Registro aprobado exitosamente');
      } else {
        const errorData = await response.json();
        alert(`Error al aprobar: ${errorData.detail}`);
      }
    } catch (err) {
      alert('Error de conexión al aprobar');
    } finally {
      setApprovingId(null);
    }
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
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando registros pendientes...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-gray-900">
              Panel de Administración
            </h1>
            <button
              onClick={() => navigate('/')}
              className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              Volver al Inicio
            </button>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
              {error}
            </div>
          )}

          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <div className="px-4 py-5 sm:px-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Registros Pendientes de Aprobación
              </h3>
              <p className="mt-1 max-w-2xl text-sm text-gray-500">
                {pendingRegistrations.length} registro(s) pendiente(s)
              </p>
            </div>

            {pendingRegistrations.length === 0 ? (
              <div className="text-center py-12">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">No hay registros pendientes</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Todos los registros han sido procesados.
                </p>
              </div>
            ) : (
              <ul className="divide-y divide-gray-200">
                {pendingRegistrations.map((registration) => (
                  <li key={registration.id} className="px-4 py-4 sm:px-6">
                    <div className="flex items-center justify-between">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <div>
                            <h4 className="text-lg font-medium text-gray-900 truncate">
                              {registration.nombre} {registration.apellido}
                            </h4>
                            <p className="text-sm text-gray-500">
                              {registration.email}
                            </p>
                          </div>
                          <div className="ml-4 flex-shrink-0">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                              registration.provider === 'google' 
                                ? 'bg-red-100 text-red-800' 
                                : 'bg-blue-100 text-blue-800'
                            }`}>
                              {registration.provider === 'google' ? 'Google' : 'Facebook'}
                            </span>
                          </div>
                        </div>
                        
                        <div className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3">
                          <div>
                            <p className="text-sm text-gray-600">
                              <span className="font-medium">Teléfono:</span> {registration.telefono || 'No especificado'}
                            </p>
                          </div>
                          <div>
                            <p className="text-sm text-gray-600">
                              <span className="font-medium">Dirección:</span> {registration.direccion || 'No especificada'}
                            </p>
                          </div>
                          <div>
                            <p className="text-sm text-gray-600">
                              <span className="font-medium">Departamento:</span> {registration.departamento || 'No especificado'}
                            </p>
                          </div>
                        </div>

                        {registration.notas_adicionales && (
                          <div className="mt-2">
                            <p className="text-sm text-gray-600">
                              <span className="font-medium">Notas:</span> {registration.notas_adicionales}
                            </p>
                          </div>
                        )}

                        <div className="mt-2">
                          <p className="text-xs text-gray-500">
                            Registrado el: {formatDate(registration.created_at)}
                          </p>
                        </div>
                      </div>

                      <div className="ml-4 flex-shrink-0">
                        <button
                          onClick={() => handleApprove(registration.id)}
                          disabled={approvingId === registration.id}
                          className="bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white px-4 py-2 rounded-md text-sm font-medium"
                        >
                          {approvingId === registration.id ? 'Aprobando...' : 'Aprobar'}
                        </button>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;
