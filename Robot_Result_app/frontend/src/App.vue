<template>
  <div id="nav">
    <NavBarComponent />
  </div >
  <div>
    <router-view class="vh-80"/>
  </div>
</template>

<script>
import NavBarComponent from "@/components/NavBar.vue";

export default {
  name: "App",

  components: {
    NavBarComponent
  },

}
</script>

<style>
body {
  font-family: 'Barlow Semi Condensed', sans-serif;
  font-weight: 300;
}
</style>
