<template>
  <div id="nav"> 
     <NavBarComponent/>
  </div>
  <router-view/>
</template>

<script>
  import { axios } from "@/common/api.service.js"
  import NavBarComponent from "@/components/NavBar.vue"
  export default{
    name: "App",

    components: {
      NavBarComponent
    },

    computed: {
      getUsername(){
          const response = axios.get("/api/v1/profile/");
          return response.results[0].username;
      }

    }
  }
</script>

<style>

  body{
    font-family: 'Barlow Semi Condensed', sans-serif;
    font-weight: 300;
  }

</style>
