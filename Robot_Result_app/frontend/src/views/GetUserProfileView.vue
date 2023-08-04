<template>
    <div>
        <button @click="getUserProfile">get prof</button>
      <h2>User Profile</h2>
      <div v-for="profile in profiles" :key="profile.username" class="profile-card">
        <h3>{{ profile.username }}</h3>
        <p><strong>Email:</strong> {{ profile.email }}</p>
        <p><strong>First Name:</strong> {{ profile.first_name }}</p>
        <p><strong>Last Name:</strong> {{ profile.last_name }}</p>
        <p v-if="profile.description"><strong>Description:</strong> {{ profile.description }}</p>
      </div>
    </div>
  </template>

<script>
import { axios } from "@/common/api.service.js";


export default{
    name: "GetUserProfileComponent",

    data() {
        return {
                profiles: []
        }
    },

    methods: {

        async getUserProfile(){
            let endpoint = "/api/v1/profile/";
            try{
                const response = await axios.get(endpoint);
                this.profiles = response.data.results;
                console.log(response);
            }catch (error){
                console.log(error.response);
                alert(error.response.statusText);
            }

        }

    }

}
</script>