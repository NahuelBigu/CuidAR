<template>



    <!-- 
    <h2 class="m-2">Cantidad de turnos por mes</h2>
    <p class="m-3">Se observa en el siguiente gráfico lineal, la cantidad de turnos que fueron solicitados en cualquier centro registrado en el sitio para cada mes del actual año.</p>
    <ve-line :data="chartData" :settings="chartSettings"></ve-line>
    <br>
    <br>
    <h2 class="m-3">Porcentajes de centros de ayuda para cada tipo</h2>
    <p>Se observa en el siguiente gráfico de torta, el porcentaje de centros de ayuda en los que se reciben donaciones para cada tipo de donación (ej: comida, ropa, transfusioens, etc).</p>
    <ve-pie :data="chartDataTorta"></ve-pie>
    <br>
    <h2 class="m-3">Cantidad de turnos solicitados para cada centro</h2>
    <p>Se observa en el siguiente gráfico de barras, la cantidad de turnos que fueron solicitados en el sitio, para cada centro de ayuda que se encuentra registrado.</p>
    <ve-histogram :data="chartDataHisto"></ve-histogram>

  -->


<div class="container-fluid mt-3">
  <div class="card">
    <div class="card-header pb-0"><h2>Estadisticas</h2></div>
    <div class="card-body bg-dark mt-1">
      <div class="row mb-4">
        <div class="col-12">
          <div class="card">
            <div class="card-header pb-0">
              <h5>Cantidad de turnos por mes</h5>
            </div>
            <div class="card-body bg-white">
              <div class="mb-3">
                <div class="row  ">
                  <div class="form-group col-6 ">
                    <div class="text-center">
                        <label  class="typo__label">Año: </label>
                      <input type="number" name="year" id="year" v-model="year" @change="modificar" required="required" style="text-align: center; " class="form-control">
                    </div>
                 </div>
                 <div class="form-group col-6">
                  
                    <label class="typo__label">Municipios: </label>
        
                    <multiselect  @input="modificar"  v-model="value" :options="options" :multiple="true" :close-on-select="false" :clear-on-select="false" :preserve-search="true" placeholder="Elegir alguno/s" label="name" track-by="name" :preselect-first="true">
                   
                      <template slot="selection" slot-scope="{ values, search, isOpen }"><span class="multiselect__single" v-if="values.length &amp;&amp; !isOpen">{{ values.length }} municipios seleccionados </span>  </template>
                      <template slot="tag">{{ '' }}</template>
                    </multiselect>
                    <div class=" mt-1">
                    <button class="btn btn-outline-danger pt-0 mx-1" style="height: 25px; " @click="clear">Ninguno <i class="fas fa-times"></i></button>
                    <button class="btn btn-outline-success pt-0" style="height: 25px; " @click="selectAll">Todos <i class="fas fa-check"></i></button>
                    </div>
                   </div>
                 
                </div>
              </div>
                <ve-line :data="chartData" :settings="chartSettings"></ve-line>
                <p class="m-3">En el gráfico lineal se observa la cantidad de turnos que fueron solicitados en cualquier centro registrado en el sitio para cada mes del año especificado.</p>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-6">
          <div class="card">
            <div class="card-header pb-0"><h5>Centros por tipo</h5></div>
            <div class="card-body bg-white">
              <ve-pie :data="chartDataTorta"></ve-pie>
              <p>En el gráfico de torta se observa el porcentaje de centros de ayuda en los que se reciben donaciones para cada tipo de donación (ej: comida, ropa, transfusioens, etc).</p>
            </div>
          </div>
        </div>
        <div class="col-6">
          <div class="card">
            <div class="card-header pb-0">
              <h5>Cantidad de turnos por centro</h5>
            </div>
            <div class="card-body bg-white">
              <ve-histogram :data="chartDataHisto"></ve-histogram>
              <p>En el gráfico de barras se observa la cantidad de turnos que fueron solicitados en el sitio, para cada centro de ayuda que se encuentra registrado.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>


<script>
import Multiselect from 'vue-multiselect'
import axios from "axios";
export default { 
  components: {
    Multiselect
  },
  data() {
    this.chartSettings = {
        area: true
      }
    return{
          year: new Date().getFullYear(),
          chartData: {
            columns: ['Mes', 'Cantidad'],
            rows: [
              {'Mes': 'Enero', 'Cantidad': 0},
              {'Mes': 'Febrero', 'Cantidad': 0},
              {'Mes': 'Marzo', 'Cantidad': 0},
              {'Mes': 'Abril', 'Cantidad': 0},
              {'Mes': 'Mayo', 'Cantidad': 0},
              {'Mes': 'Junio', 'Cantidad': 0},
              {'Mes': 'Julio', 'Cantidad': 0},
              {'Mes': 'Agosto', 'Cantidad': 0},
              {'Mes': 'Septiembre', 'Cantidad': 0},
              {'Mes': 'Octubre', 'Cantidad': 0},
              {'Mes': 'Noviembre', 'Cantidad': 0},
              {'Mes': 'Diciembre', 'Cantidad': 0}
            ]
          },
          chartDataTorta: {
          columns: ['Tipos', 'Cantidad'],
          rows: [
            { 'Tipos': 'Ropa', 'Cantidad': 0 },
            { 'Tipos': 'Comida', 'Cantidad': 0 },
            { 'Tipos': 'Sangre', 'Cantidad': 0 }
          ]
          },
          chartDataHisto: {
            columns: ['Centro', 'Cantidad'],
            rows: []
          },
          value: [],
          valuesId:[],
          options: []
          
        }      
  },
  methods: {
        modificar() { 
            axios
            .get("https://admin-grupo72.proyecto2020.linti.unlp.edu.ar/estadisticas/turnos_por_fechas?fechaIni="+this.year.toString()+"-01-01&fechaFin="+this.year.toString()+"-12-31")
            .then(res => { 
              for (let index = 0; index < 12; index++) {
                this.chartData.rows[index]["Cantidad"]=0
              }
              var valuesId= this.value.map(function(x) {
                                              return x["id"];
                                            })
                                            
              for (var x in res.data){
                
                if ( valuesId.includes(parseInt(res.data[x]["Municipio"]))){
                  
                  this.chartData.rows[new Date(res.data[x]["Fecha"]).getMonth()]["Cantidad"]+=1
                }
              }
              })
            },
        clear(){
          this.value=[]
          this.modificar()
        },
        selectAll(){
          this.value=this.options
          this.modificar()
        }
  },
  mounted(){

    axios.get('https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=150')
        .then(Response=>{
          for (let index = 1; index <= 135; index++) {
            this.options.push(Response.data.data.Town[index])
          }
          this.value=[]
          }) 


    axios
      .get("https://admin-grupo72.proyecto2020.linti.unlp.edu.ar/centros?perPage=99999999")
      .then(text => {
        var aux={
          'Ropa':0,
          'Comida':0,
          'Sangre':0
        }
       for (var i in text.data.helpcenters){
          for (var j in text.data.helpcenters[i].type_center){
            aux[text.data.helpcenters[i].type_center[j]]++
          }

       }
       
        this.chartDataTorta.rows[0]["Cantidad"]=aux['Ropa']
        this.chartDataTorta.rows[1]["Cantidad"]=aux['Comida']
        this.chartDataTorta.rows[2]["Cantidad"]=aux['Sangre']
      
      })  

      axios
      .get("https://admin-grupo72.proyecto2020.linti.unlp.edu.ar/estadisticas/turnos_por_fechas?fechaIni="+this.year.toString()+"-01-01&fechaFin="+(new Date().getFullYear()+1).toString()+"-01-01")
      .then(res => { 
        var actualYear=new Date().getFullYear()
        for (var x in res.data){
          if (new Date(x).getFullYear()==actualYear) {
            this.chartData.rows[new Date(x).getMonth()]["Cantidad"]+=res.data[x]
          }
        }
        })
      
      axios
      .get("https://admin-grupo72.proyecto2020.linti.unlp.edu.ar/estadisticas/turnos_por_centros")
      .then(
        res=>{
          for (var x in res.data){
            this.chartDataHisto.rows.push({"Centro":x ,"Cantidad":res.data[x]})
   
        }
        }
      )
     

  }
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style>
</style>