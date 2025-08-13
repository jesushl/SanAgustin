// Servicio mock para modo demo
// Simula las respuestas del backend sin necesidad de conexión real

export interface DemoPanelResidente {
  departamento: {
    id: number;
    numero: string;
    usuario_id: number;
  };
  estacionamiento?: {
    id: number;
    numero: string;
    placa?: string;
    modelo_auto?: string;
    color_auto?: string;
    es_visita: boolean;
    departamento_id: number;
  };
  adeudos_pendientes: Array<{
    id: number;
    departamento_id: number;
    monto: number;
    descripcion: string;
    fecha_vencimiento: string;
    fecha_creacion: string;
    pagado: boolean;
  }>;
  total_adeudos: number;
  puede_reservar: boolean;
}

export interface DemoAreaComun {
  id: number;
  nombre: string;
  descripcion: string;
  ubicacion: string;
  capacidad: number;
}

export interface DemoReservaAreaComun {
  id: number;
  area_comun_id: number;
  departamento_id: number;
  periodo_inicio: string;
  periodo_fin: string;
  estado: string;
  area_comun: DemoAreaComun;
}

export interface DemoLugarVisita {
  id: number;
  numero: string;
  descripcion: string;
  capacidad: number;
}

export interface DemoReservaVisita {
  id: number;
  lugar_visita_id: number;
  departamento_id: number;
  placa_visita?: string;
  periodo_inicio: string;
  periodo_fin: string;
  estado: string;
  lugar_visita: DemoLugarVisita;
}

class DemoService {
  private delay(ms: number = 500): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Panel de residente
  async getPanelResidente(): Promise<{ data: DemoPanelResidente }> {
    await this.delay();
    return {
      data: {
        departamento: {
          id: 1,
          numero: "A1",
          usuario_id: 1
        },
        estacionamiento: {
          id: 1,
          numero: "E1",
          placa: "ABC-123",
          modelo_auto: "Toyota Corolla",
          color_auto: "Blanco",
          es_visita: false,
          departamento_id: 1
        },
        adeudos_pendientes: [
          {
            id: 1,
            departamento_id: 1,
            monto: 1500,
            descripcion: "Mantenimiento mensual",
            fecha_vencimiento: "2024-09-15",
            fecha_creacion: "2024-08-01",
            pagado: false
          }
        ],
        total_adeudos: 1500,
        puede_reservar: true
      }
    };
  }

  // Áreas comunes
  async getAreasComunes(): Promise<{ data: DemoAreaComun[] }> {
    await this.delay();
    return {
      data: [
        {
          id: 1,
          nombre: "Palapa",
          descripcion: "Área de recreación con palapa y asadores",
          ubicacion: "Zona central",
          capacidad: 20
        },
        {
          id: 2,
          nombre: "Sala de eventos",
          descripcion: "Sala para eventos sociales",
          ubicacion: "Edificio principal",
          capacidad: 50
        },
        {
          id: 3,
          nombre: "Gimnasio",
          descripcion: "Gimnasio equipado",
          ubicacion: "Edificio B",
          capacidad: 15
        }
      ]
    };
  }

  async verificarDisponibilidadAreaComun(
    areaComunId: number, 
    fechaInicio: string, 
    fechaFin: string
  ): Promise<{ data: { disponible: boolean; reservas_existentes: number } }> {
    await this.delay();
    return {
      data: {
        disponible: true,
        reservas_existentes: 0
      }
    };
  }

  async crearReservaAreaComun(reserva: {
    area_comun_id: number;
    periodo_inicio: string;
    periodo_fin: string;
  }): Promise<{ data: DemoReservaAreaComun }> {
    await this.delay();
    return {
      data: {
        id: Math.floor(Math.random() * 1000),
        area_comun_id: reserva.area_comun_id,
        departamento_id: 1,
        periodo_inicio: reserva.periodo_inicio,
        periodo_fin: reserva.periodo_fin,
        estado: "activa",
        area_comun: {
          id: reserva.area_comun_id,
          nombre: "Palapa",
          descripcion: "Área de recreación",
          ubicacion: "Zona central",
          capacidad: 20
        }
      }
    };
  }

  async getReservasAreaComunUsuario(): Promise<{ data: DemoReservaAreaComun[] }> {
    await this.delay();
    return {
      data: [
        {
          id: 1,
          area_comun_id: 1,
          departamento_id: 1,
          periodo_inicio: "2024-08-15T10:00:00",
          periodo_fin: "2024-08-15T14:00:00",
          estado: "activa",
          area_comun: {
            id: 1,
            nombre: "Palapa",
            descripcion: "Área de recreación con palapa y asadores",
            ubicacion: "Zona central",
            capacidad: 20
          }
        }
      ]
    };
  }

  // Lugares de visita
  async getLugaresVisita(): Promise<{ data: DemoLugarVisita[] }> {
    await this.delay();
    return {
      data: [
        {
          id: 1,
          numero: "V1",
          descripcion: "Estacionamiento de visita principal",
          capacidad: 5
        },
        {
          id: 2,
          numero: "V2",
          descripcion: "Estacionamiento de visita secundario",
          capacidad: 3
        }
      ]
    };
  }

  async verificarDisponibilidadLugarVisita(
    lugarVisitaId: number, 
    fechaInicio: string, 
    fechaFin: string
  ): Promise<{ data: { disponible: boolean; reservas_existentes: number } }> {
    await this.delay();
    return {
      data: {
        disponible: true,
        reservas_existentes: 0
      }
    };
  }

  async crearReservaVisita(reserva: {
    lugar_visita_id: number;
    placa_visita?: string;
    periodo_inicio: string;
    periodo_fin: string;
  }): Promise<{ data: DemoReservaVisita }> {
    await this.delay();
    return {
      data: {
        id: Math.floor(Math.random() * 1000),
        lugar_visita_id: reserva.lugar_visita_id,
        departamento_id: 1,
        placa_visita: reserva.placa_visita,
        periodo_inicio: reserva.periodo_inicio,
        periodo_fin: reserva.periodo_fin,
        estado: "activa",
        lugar_visita: {
          id: reserva.lugar_visita_id,
          numero: "V1",
          descripcion: "Estacionamiento de visita principal",
          capacidad: 5
        }
      }
    };
  }

  async getReservasVisitaUsuario(): Promise<{ data: DemoReservaVisita[] }> {
    await this.delay();
    return {
      data: [
        {
          id: 1,
          lugar_visita_id: 1,
          departamento_id: 1,
          placa_visita: "XYZ-789",
          periodo_inicio: "2024-08-16T09:00:00",
          periodo_fin: "2024-08-16T18:00:00",
          estado: "activa",
          lugar_visita: {
            id: 1,
            numero: "V1",
            descripcion: "Estacionamiento de visita principal",
            capacidad: 5
          }
        }
      ]
    };
  }

  // Estacionamiento
  async actualizarEstacionamiento(
    estacionamientoId: number, 
    datos: {
      placa?: string;
      modelo_auto?: string;
      color_auto?: string;
    }
  ): Promise<{ data: any }> {
    await this.delay();
    return {
      data: {
        id: estacionamientoId,
        ...datos,
        mensaje: "Estacionamiento actualizado en modo demo"
      }
    };
  }
}

export const demoService = new DemoService();
