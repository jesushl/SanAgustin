import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Car, 
  Users, 
  Calendar, 
  DollarSign, 
  QrCode,
  Clock
} from 'lucide-react';

const Home: React.FC = () => {
  const stats = [
    {
      name: 'Estacionamientos',
      value: '24',
      icon: Car,
      color: 'bg-blue-500',
      href: '/estacionamientos'
    },
    {
      name: 'Contactos',
      value: '48',
      icon: Users,
      color: 'bg-green-500',
      href: '/contactos'
    },
    {
      name: 'Reservas Activas',
      value: '12',
      icon: Calendar,
      color: 'bg-purple-500',
      href: '/reservas'
    },
    {
      name: 'Adeudos Pendientes',
      value: '8',
      icon: DollarSign,
      color: 'bg-red-500',
      href: '/adeudos'
    }
  ];

  const quickActions = [
    {
      name: 'Registrar Visita',
      description: 'Registrar un vehículo de visita',
      icon: Car,
      href: '/estacionamientos',
      color: 'bg-blue-50 text-blue-700 hover:bg-blue-100'
    },
    {
      name: 'Nueva Reserva',
      description: 'Reservar área común',
      icon: Calendar,
      href: '/reservas',
      color: 'bg-green-50 text-green-700 hover:bg-green-100'
    },
    {
      name: 'Generar QR',
      description: 'Generar código QR para estacionamiento',
      icon: QrCode,
      href: '/qr',
      color: 'bg-purple-50 text-purple-700 hover:bg-purple-100'
    },
    {
      name: 'Registrar Adeudo',
      description: 'Registrar nuevo adeudo',
      icon: DollarSign,
      href: '/adeudos',
      color: 'bg-red-50 text-red-700 hover:bg-red-100'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Bienvenido a San Agustín
          </h1>
          <p className="mt-2 text-gray-600">
            Sistema de gestión de servicios para la privada San Agustín
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat) => {
            const Icon = stat.icon;
            return (
              <Link
                key={stat.name}
                to={stat.href}
                className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200"
              >
                <div className="flex items-center">
                  <div className={`${stat.color} p-3 rounded-lg`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                    <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Acciones Rápidas
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {quickActions.map((action) => {
              const Icon = action.icon;
              return (
                <Link
                  key={action.name}
                  to={action.href}
                  className={`${action.color} p-6 rounded-lg border transition-colors duration-200`}
                >
                  <div className="flex items-center">
                    <Icon className="w-8 h-8 mr-4" />
                    <div>
                      <h3 className="font-semibold">{action.name}</h3>
                      <p className="text-sm opacity-75">{action.description}</p>
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Actividad Reciente
          </h2>
          <div className="space-y-4">
            <div className="flex items-center p-4 bg-gray-50 rounded-lg">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-4"></div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">
                  Nueva reserva de área común
                </p>
                <p className="text-sm text-gray-600">
                  Departamento 101 reservó la palapa para el 15 de agosto
                </p>
              </div>
              <Clock className="w-4 h-4 text-gray-400" />
            </div>
            
            <div className="flex items-center p-4 bg-gray-50 rounded-lg">
              <div className="w-2 h-2 bg-blue-500 rounded-full mr-4"></div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">
                  Vehículo de visita registrado
                </p>
                <p className="text-sm text-gray-600">
                  Placa ABC-123 registrada para visita al departamento 205
                </p>
              </div>
              <Clock className="w-4 h-4 text-gray-400" />
            </div>
            
            <div className="flex items-center p-4 bg-gray-50 rounded-lg">
              <div className="w-2 h-2 bg-red-500 rounded-full mr-4"></div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">
                  Nuevo adeudo registrado
                </p>
                <p className="text-sm text-gray-600">
                  Departamento 303 tiene un adeudo pendiente de $1,500
                </p>
              </div>
              <Clock className="w-4 h-4 text-gray-400" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
