export interface Estacionamiento {
  numero_estacionamiento: string;
  placa: string;
  modelo: string;
  color: string;
  es_visita: boolean;
}

export interface Contacto {
  nombre: string;
  apellido: string;
  numero_contacto: string;
  correo: string;
}

export interface ContactoResidente {
  id: number;
  nombre: string;
  apellido: string;
  numero_contacto: string;
  correo_electronico: string;
}

export interface ReservaAreaComun {
  id: number;
  area: string;
  periodo_inicio: string;
  periodo_fin: string;
  departamento_id: number;
}

export interface ReservaAreaComunCreate {
  area: string;
  periodo_inicio: string;
  periodo_fin: string;
  departamento_id: number;
}

export interface ReservaVisita {
  numero_departamento: string;
  placas_visita: string;
  hora_llegada: string;
  horas_estancia: number;
}

export interface Adeudo {
  id: number;
  departamento_id: number;
  monto: number;
  descripcion: string;
  fecha: string;
}

export interface AdeudoCreate {
  departamento_id: number;
  monto: number;
  descripcion: string;
}

export interface Departamento {
  id: number;
  numero: string;
  contacto_id?: number;
}

export interface AreaComun {
  id: number;
  nombre: string;
  descripcion: string;
  ubicacion: string;
}
