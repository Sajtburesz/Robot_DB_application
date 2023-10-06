<template>
    <div>
      <h2>User Profile</h2>
      <div v-for="profile in profiles" :key="profile.username" class="profile-card">
        <h3>{{ profile.username }}</h3>
        <p><strong>Email:</strong> {{ profile.email }}</p>
        <p><strong>First Name:</strong> {{ profile.first_name }}</p>
        <p><strong>Last Name:</strong> {{ profile.last_name }}</p>
        <p v-if="profile.description"><strong>Description:</strong> {{ profile.description }}</p>
      </div>
    <router-link class="btn" :to="{ name: 'EditUserProfile' }" >Edit</router-link>
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
    created(){
        this.getUserProfile();
    },

    methods: {
        async getUserAvatar(){
            let endpoint = "/api/v1/avatar/"
            try{
                const resp = await axios.get(enpoint);
                
            }catch (error){
                console.log(error.response);
                alert(error.response.statusText);
            }
        },

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