<template>
  <div>
    <ul>
        <li v-for="centro in centros" v-bind:key="centro.name">
           {{centro.name}}
        </li>

    </ul>
    <h1>{{ title }}</h1>
    
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      centros: []
    };
  },
    mounted() {
      axios
        .get("https://admin-grupo72.proyecto2020.linti.unlp.edu.ar/centros")
        .then((response) => ( this.centros = response.data.helpcenters));
       
    }
 
};
</script>

<style media="screen">
</style>