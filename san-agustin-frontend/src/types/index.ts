// Tipos para el panel de residente
export interface Departamento {
  id: number;
  numero: string;
  usuario_id?: number;
}

export interface Estacionamiento {
  id: number;
  numero: string;
  placa?: string;
  modelo_auto?: string;
  color_auto?: string;
  es_visita: boolean;
  departamento_id: number;
}

export interface Adeudo {
  id: number;
  departamento_id: number;
  monto: number;
  descripcion: string;
  fecha_vencimiento: string;
  fecha_creacion: string;
  pagado: boolean;
}

export interface PanelResidente {
  departamento: Departamento;
  estacionamiento?: Estacionamiento;
  adeudos_pendientes: Adeudo[];
  total_adeudos: number;
  puede_reservar: boolean;
}

// Tipos para áreas comunes
export interface AreaComun {
  id: number;
  nombre: string;
  descripcion: string;
  ubicacion: string;
  capacidad: number;
}

export interface ReservaAreaComun {
  id: number;
  area_comun_id: number;
  departamento_id: number;
  periodo_inicio: string;
  periodo_fin: string;
  estado: string;
  area_comun: AreaComun;
}

export interface ReservaAreaComunCreate {
  area_comun_id: number;
  periodo_inicio: string;
  periodo_fin: string;
}

// Tipos para lugares de visita
export interface LugarVisita {
  id: number;
  numero: string;
  descripcion: string;
  capacidad: number;
}

export interface ReservaVisita {
  id: number;
  lugar_visita_id: number;
  departamento_id: number;
  placa_visita?: string;
  periodo_inicio: string;
  periodo_fin: string;
  estado: string;
  lugar_visita: LugarVisita;
}

export interface ReservaVisitaCreate {
  lugar_visita_id: number;
  placa_visita?: string;
  periodo_inicio: string;
  periodo_fin: string;
}

// Tipos para disponibilidad
export interface Disponibilidad {
  disponible: boolean;
  reservas_existentes: number;
}

// Tipos para actualización de estacionamiento
export interface EstacionamientoUpdate {
  placa?: string;
  modelo_auto?: string;
  color_auto?: string;
}
