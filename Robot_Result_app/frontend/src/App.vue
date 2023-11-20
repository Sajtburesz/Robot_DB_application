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

import { axios } from "@/common/api.service.js";

export default {
  name: "App",

  components: {
    NavBarComponent
  },
  created() {
    this.fetchAdminStatus();
    this.intervalID = setInterval(this.fetchAdminStatus, 300000);
  },
  methods: {
    async fetchAdminStatus() {
      try {
        const response = await axios.get('/api/v1/check-admin-status/');

        let isAdmin = false;
        if(response.data.is_superuser){
          isAdmin = true;
        }else{
          isAdmin = false;
        }
        this.$store.dispatch('updateAdminStatus', isAdmin);
      } catch (error) {
        console.error("Error fetching admin status:", error);
      }
    }
  }

}
</script>

<style>
body {
  font-family: 'Barlow Semi Condensed', sans-serif;
  font-weight: 300;
}
</style>
