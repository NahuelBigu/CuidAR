<template>
  <div class="m-5">
    <!-- Button trigger modal -->
    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModalCenter">
    Nuevo Turno
    </button>

    <!-- Modal -->
    <div class="modal fade" id="exampleModalCenter" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">Solicitando turno</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <div class="modal-body">
            <div>
                <p style="color:red" v-if="error">{{ error_message }}</p>
                <p style="color:green" v-if="success_state">{{ success }}</p>
            </div>
            <form>
                <div class="my-2">
                    <span>Fecha: </span>
                    <input type="date" name="date" id="date" v-model="turno.fecha" @change="modificar" required>
                </div>
                <div class="my-2">
                    <span>Horario de inicio: </span>
                    <select v-model="turno.hora_inicio" @change="mod_closing_time" required>
                        <option v-for="option in hora_inicios" v-bind:key="option" v-bind:value="option">
                            {{ option.slice(0,-3) }}
                        </option>
                    </select>
                </div>
                <div class="my-2"><span>Horario de fin: </span><span>{{turno.hora_fin}}</span></div>
                <div class="my-2">
                    <span>Email: </span><input type="email" name="email_donante" id="email_donante" v-model="turno.email_donante" required>
                </div>
                <div class="my-2">
                    <span>Telefono: </span><input type="tel" name="telefono_donante" id="telefono_donante" v-model="turno.telefono_donante" required>
                </div>
                <div class="my-2">
                    <span>Nombre: </span><input type="text" name="nombre_donante" id="nombre_donante" v-model="turno.nombre_donante" required>
                </div>
                <div class="my-2">
                    <span>Apellido: </span><input type="text" name="apellido_donante" id="apellido_donante" v-model="turno.apellido_donante" required>
                </div>
            </form>
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>
            <button type="button" class="btn btn-primary" @click="mandar">Solicitar turno</button>
        </div>
        </div>
    </div>
    </div>
    
  </div>
</template>
<script>
import axios from "axios";
export default { 
    data() {
        return{
            turno: {
                centro_id: 1,
                hora_inicio: "",
                hora_fin: "",
                email_donante:"",
                telefono_donante:"",
                nombre_donante:"",
                apellido_donante:"",
                fecha: ""
            },
            error: false,
            success_state: false,
            error_message: '',
            hora_inicios: []
        }
    },
    methods: {
        mandar() { 
            if (this.turno.telefono_donante=="") {
                this.error=true;
                this.error_message='Se necesita especificar un telefono del donante'
                return
            }
            if (this.turno.email_donante=="") {
                this.error=true;
                this.error_message='Se necesita especificar un email del donante'
                return
            }
            if (this.turno.fecha=="") {
                this.error=true;
                this.error_message='Se necesita especificar una fecha del turno'
            }
            else {
                if (this.turno.hora_inicio=="") {
                    this.error=true;
                    this.error_message='Se necesita especificar una hora del turno'
                }
                else { 
                    var turn = {
                        centro_id: this.turno.centro_id,
                        hora_inicio: this.turno.hora_inicio,
                        hora_fin: this.turno.hora_fin,
                        email_donante: this.turno.email_donante,
                        nombre_donante: this.turno.nombre_donante,
                        apellido_donante: this.turno.apellido_donante,
                        telefono_donante: this.turno.telefono_donante,
                        fecha: this.turno.fecha
                    }
                    axios.post('https://admin-grupo72.proyecto2020.linti.unlp.edu.ar/centros/'+this.centro_id2+'/reserva', turn)
                    this.hora_inicios=[]
                    this.success="El turno se solicito correctamente"
                    this.success_state=true
                    this.error=false
                    this.error_message=""
                    this.turno.centro_id=1
                    this.turno.hora_inicio=""
                    this.turno.hora_fin=""
                    this.turno.nombre_donante=""
                    this.turno.apellido_donante=""
                    this.turno.email_donante=""
                    this.turno.telefono_donante=""
                    this.turno.fecha=""
                }
            }             
        },
        modificar() {
            this.hora_inicio=axios
            .get('https://admin-grupo72.proyecto2020.linti.unlp.edu.ar/turnos/disponibles/'+this.turno.centro_id+'/'+(this.turno.fecha).replaceAll('-',''))
            .then(response => (this.hora_inicios = response.data))
        },
        mod_closing_time() {
            this.turno.hora_fin = new Date(new Date("1970/01/01 " + this.turno.hora_inicio).getTime() + 30 * 60000).toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit', hour12: false });
        }        
    },
    props:{
        centro_id2:{type: Number}
    }
};
</script>

<style>
</style>