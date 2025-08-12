import api from '../config/api';
import type {
  Estacionamiento,
  ContactoResidente,
  ReservaAreaComun,
  ReservaAreaComunCreate,
  ReservaVisita,
  Adeudo,
  AdeudoCreate
} from '../types';

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
