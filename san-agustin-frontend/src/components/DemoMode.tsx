import React from 'react';
import { useAuth } from '../contexts/AuthContext';

interface DemoModeProps {
  onClose: () => void;
}

const DemoMode: React.FC<DemoModeProps> = ({ onClose }) => {
  const { login } = useAuth();

  const loginAsResidente = () => {
    const demoUser = {
      token: 'demo_token_residente',
      userId: 1,
      email: 'residente@test.com',
      isAdmin: false
    };
    login(demoUser);
    onClose();
  };

  const loginAsAdmin = () => {
    const demoAdmin = {
      token: 'demo_token_admin',
      userId: 2,
      email: 'admin@test.com',
      isAdmin: true
    };
    login(demoAdmin);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4">
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            🏠 Modo Demo - San Agustín
          </h2>
          <p className="text-gray-600">
            Accede al sistema sin registro para explorar las funcionalidades
          </p>
        </div>

        <div className="space-y-4">
          {/* Usuario Residente */}
          <div className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-gray-900">👤 Usuario Residente</h3>
                <p className="text-sm text-gray-600">residente@test.com</p>
                <p className="text-xs text-gray-500 mt-1">
                  Acceso a: Panel de residente, reservas de áreas comunes y visitas
                </p>
              </div>
              <button
                onClick={loginAsResidente}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Acceder
              </button>
            </div>
          </div>

          {/* Administrador */}
          <div className="border border-gray-200 rounded-lg p-4 hover:border-green-300 transition-colors">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-gray-900">👨‍💼 Administrador</h3>
                <p className="text-sm text-gray-600">admin@test.com</p>
                <p className="text-xs text-gray-500 mt-1">
                  Acceso completo: Panel de admin, aprobación de registros, gestión
                </p>
              </div>
              <button
                onClick={loginAsAdmin}
                className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Acceder
              </button>
            </div>
          </div>
        </div>

        <div className="mt-6 pt-4 border-t border-gray-200">
          <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-yellow-800">
                  <strong>Modo Demo:</strong> Los datos mostrados son simulados. 
                  Las acciones no se guardarán permanentemente.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6 flex justify-center">
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-sm font-medium transition-colors"
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>
  );
};

export default DemoMode;
