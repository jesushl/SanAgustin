import api from '../config/api';
import { demoService } from './demoService';
import type {
  Estacionamiento,
  ContactoResidente,
  ReservaAreaComun,
  ReservaAreaComunCreate,
  ReservaVisita,
  Adeudo,
  AdeudoCreate
} from '../types';

const API_BASE_URL = 'http://localhost:8000';

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

// Función para detectar si estamos en modo demo
const isDemoMode = (): boolean => {
  const token = localStorage.getItem('token');
  return token === 'demo_token_residente' || token === 'demo_token_admin';
};

class ApiService {
  private getHeaders(): HeadersInit {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    };
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: this.getHeaders(),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      return { error: error instanceof Error ? error.message : 'Error desconocido' };
    }
  }

  // Panel de residente
  async getPanelResidente() {
    if (isDemoMode()) {
      return demoService.getPanelResidente();
    }
    return this.request('/panel-residente');
  }

  // Áreas comunes
  async getAreasComunes() {
    if (isDemoMode()) {
      return demoService.getAreasComunes();
    }
    return this.request('/areas-comunes');
  }

  async verificarDisponibilidadAreaComun(areaComunId: number, fechaInicio: string, fechaFin: string) {
    if (isDemoMode()) {
      return demoService.verificarDisponibilidadAreaComun(areaComunId, fechaInicio, fechaFin);
    }
    const params = new URLSearchParams({
      area_comun_id: areaComunId.toString(),
      fecha_inicio: fechaInicio,
      fecha_fin: fechaFin
    });
    return this.request(`/reservas-area-comun/disponibilidad?${params}`);
  }

  async crearReservaAreaComun(reserva: {
    area_comun_id: number;
    periodo_inicio: string;
    periodo_fin: string;
  }) {
    if (isDemoMode()) {
      return demoService.crearReservaAreaComun(reserva);
    }
    return this.request('/reservas-area-comun', {
      method: 'POST',
      body: JSON.stringify(reserva)
    });
  }

  async getReservasAreaComunUsuario() {
    if (isDemoMode()) {
      return demoService.getReservasAreaComunUsuario();
    }
    return this.request('/reservas-area-comun/usuario');
  }

  // Lugares de visita
  async getLugaresVisita() {
    if (isDemoMode()) {
      return demoService.getLugaresVisita();
    }
    return this.request('/lugares-visita');
  }

  async verificarDisponibilidadLugarVisita(lugarVisitaId: number, fechaInicio: string, fechaFin: string) {
    if (isDemoMode()) {
      return demoService.verificarDisponibilidadLugarVisita(lugarVisitaId, fechaInicio, fechaFin);
    }
    const params = new URLSearchParams({
      lugar_visita_id: lugarVisitaId.toString(),
      fecha_inicio: fechaInicio,
      fecha_fin: fechaFin
    });
    return this.request(`/reservas-visita/disponibilidad?${params}`);
  }

  async crearReservaVisita(reserva: {
    lugar_visita_id: number;
    placa_visita?: string;
    periodo_inicio: string;
    periodo_fin: string;
  }) {
    if (isDemoMode()) {
      return demoService.crearReservaVisita(reserva);
    }
    return this.request('/reservas-visita', {
      method: 'POST',
      body: JSON.stringify(reserva)
    });
  }

  async getReservasVisitaUsuario() {
    if (isDemoMode()) {
      return demoService.getReservasVisitaUsuario();
    }
    return this.request('/reservas-visita/usuario');
  }

  // Estacionamiento
  async actualizarEstacionamiento(estacionamientoId: number, datos: {
    placa?: string;
    modelo_auto?: string;
    color_auto?: string;
  }) {
    if (isDemoMode()) {
      return demoService.actualizarEstacionamiento(estacionamientoId, datos);
    }
    return this.request(`/estacionamiento/${estacionamientoId}`, {
      method: 'PUT',
      body: JSON.stringify(datos)
    });
  }
}

export const apiService = new ApiService();

// Servicios de Estacionamientos
export const estacionamientoService = {
  obtenerPorNumero: (numero: string): Promise<Estacionamiento> =>
    api.get(`/estacionamientos/${numero}`).then(res => res.data),
  
  validarPlaca: (placa: string): Promise<any> =>
    api.get(`/placas/${placa}`).then(res => res.data),
  
  obtenerResidente: (id: number): Promise<Estacionamiento> =>
    api.get(`/estacionamientos_residentes/${id}`).then(res => res.data),
  
  obtenerPorPlaca: (placa: string): Promise<Estacionamiento> =>
    api.get(`/placas_residentes/${placa}`).then(res => res.data),
};

// Servicios de Contactos
export const contactoService = {
  obtenerTodos: (): Promise<ContactoResidente[]> =>
    api.get('/contactos_residente/').then(res => res.data),
  
  obtenerPorId: (id: number): Promise<ContactoResidente> =>
    api.get(`/contactos_residente/${id}`).then(res => res.data),
  
  crear: (contacto: Omit<ContactoResidente, 'id'>): Promise<ContactoResidente> =>
    api.post('/contactos_residente/', contacto).then(res => res.data),
};

// Servicios de Reservas de Áreas Comunes
export const reservaAreaComunService = {
  obtenerTodas: (): Promise<ReservaAreaComun[]> =>
    api.get('/reservas_area_comun/').then(res => res.data),
  
  crear: (reserva: ReservaAreaComunCreate): Promise<ReservaAreaComun> =>
    api.post('/reservas_area_comun/', reserva).then(res => res.data),
};

// Servicios de Reservas de Visitas
export const reservaVisitaService = {
  crearAutomatica: (reserva: ReservaVisita): Promise<any> =>
    api.post('/reservas_visitas/', reserva).then(res => res.data),
};

// Servicios de Adeudos
export const adeudoService = {
  obtenerTodos: (): Promise<Adeudo[]> =>
    api.get('/adeudos/').then(res => res.data),
  
  obtenerPorDepartamento: (departamentoId: number): Promise<Adeudo[]> =>
    api.get(`/adeudos/${departamentoId}`).then(res => res.data),
  
  crear: (adeudo: AdeudoCreate): Promise<Adeudo> =>
    api.post('/adeudos/', adeudo).then(res => res.data),
};

// Servicios de QR
export const qrService = {
  generarEstacionamiento: (estacionamiento: Estacionamiento): Promise<any> =>
    api.post('/estacionamiento_qr/', estacionamiento).then(res => res.data),
  
  leerVehiculo: (qrData: string): Promise<any> =>
    api.post('/vehiculo_qr_info/', { qr_data: qrData }).then(res => res.data),
};
