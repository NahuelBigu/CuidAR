<template>
  <div>

    <header class="titulo text-white pt-5 pb-5">
      <div class="container text-center">
        <h1>Centros de ayuda de la provincia de Buenos Aires</h1>
      </div>
    </header>

    <div class="row">
      <div class="col-8 offset-2">
        <h5 class="text-center mt-3"></h5>
      </div>
    </div>

    
      <div class="container">
      <div class="row mt-3">
        <div class="col-lg-4 d-flex align-items-stretch">
        <router-link class="card list-group-item list-group-item-action" to="/mapa" >
          <div class="card-body">
            <h3>Mapa</h3>
            <hr>
            <p>Mapa interactivo con ubicaciones de todos los centros de ayuda de la provincia</p>
            <br>
          <img src="/img/map.svg" alt="Imagen de Mapa" class="imagenCard ">
          </div>
        </router-link>
      </div>

      <div class="col-lg-4 d-flex align-items-stretch">
        <router-link class="card list-group-item list-group-item-action" to="/estadisticas">
          <div class="card-body">
            <h3>Estadisticas</h3>
            <hr>
            <p>Estadisticas de los centros de ayuda, turnos solicitados por municipio, etc</p>
            <br><br><br>
             <img src="/img/estadistics.svg" alt="Imagen de Estadisticas" class="imagenCard ">
          </div>
     
           
          
        </router-link>
      </div>

      <div class="col-lg-4 d-flex align-items-stretch" >
        <router-link class="card list-group-item list-group-item-action" to="/nuevocentro" >
          <div class="card-body">
            <h3>Nuevo centro</h3>
            <hr>
            <p>Introduzca los datos de su centro de ayuda para que, luego de una revicion de nuestros operadores, entre al sistema</p>
            <img src="/img/newcenter.svg" alt="Imagen de Nuevo Centro" class="imagenCard ">
          </div>
          
            
    
        </router-link>
      </div>
    </div>
      </div>
      
    
  </div>
</template>
<script>
export default { 
};
</script>

<style>
.titulo {
 
  background: #28a745; /* fallback for old browsers */
 
  background: linear-gradient(to bottom,#28a745, #165d27); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
.imagenCard {
  height: 100%;
  width: 100%;
  position: relative;; 

}
</style>