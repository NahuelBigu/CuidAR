<template>
  <nav
    class="navbar navbar-dark navbar-expand-md bg-success justify-content-between"
    style="background-color: rgb(105, 175, 255)"
  >
    <div class="container-fluid">
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target=".dual-nav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="navbar-collapse collapse dual-nav w-50 order-1 order-md-0">
        <ul class="navbar-nav">
          <li class="nav-item is-active ">
            <router-link active-class="is-active" to="/" class="nav-link pl-0"> Home </router-link>
          </li>
          <li class="nav-item is-active">
            <router-link active-class="is-active" to="/mapa" class="nav-link pl-0"> Mapa </router-link>
          </li>
          <li class="nav-item is-active">
            <router-link active-class="is-active" to="/estadisticas" class="nav-link pl-0">
              Estadisticas
            </router-link>
          </li>
          <li class="nav-item is-active">
            <router-link active-class="is-active" to="/nuevocentro" class="nav-link pl-0">
              Nuevo Centro
            </router-link>
          </li>
        </ul>
      </div>
      
      <router-link to="/" class="navbar-brand mx-auto d-block text-center order-0 order-md-1 display-5"> Cuid<strong>AR</strong> </router-link>
      <div class="navbar-collapse collapse dual-nav w-50 order-2">
        
      </div>
    </div>
  </nav>
</template>

<script>

export default {
 
};
</script>

<style>
</style>