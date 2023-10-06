<template>
    <div>
        <h2>Edit Profile</h2>
        <form @submit.prevent="saveProfile">
            <div>
                <label for="username">Username</label>
                <input v-model="profile.username" type="text" id="username" readonly />
            </div>
            <div>
                <label for="first_name">First Name</label>
                <input v-model="profile.first_name" type="text" id="first_name" :placeholder="profile.first_name" />
            </div>
            <div>
                <label for="last_name">Last Name</label>
                <input v-model="profile.last_name" type="text" id="last_name" />
            </div>
            <div>
                <label for="email">Email</label>
                <input v-model="profile.email" type="text" id="email" />
            </div>
            <div>
                <label for="description">Description</label>
                <input v-model="profile.description" type="text" id="description" />
            </div>
            <button type="submit">Save Profile</button>
        </form>
    </div>
</template>
  
<script>
import { axios } from "@/common/api.service.js"
export default {
    data() {
        return {
            profile: {
                username: "",
                first_name: "",
                last_name: "",
                email: "",
                description: "",
            },
        };
    },
    beforeRouteEnter(to, from, next) {
        // Call your specific function here
        next((vm) => {
            vm.getUserProfile();
        });
    },
    methods: {
        async getUserProfile() {
            // Fetch user profile data from Django backend
            try {
                const response = await axios.get(`/api/v1/profiles/sajtburesz/`);
                this.profile = response.data;
            } catch (error) {
                console.error("Error fetching profile data:", error);
            }
        },
        async saveProfile() {
            // Update user profile data on the Django backend
            try {
                await axios.put(`/api/v1/profiles/sajtburesz/`, this.profile);
                console.log("Profile data updated successfully");
            } catch (error) {
                console.error("Error updating profile data:", error);
            }
        },
    },
};
</script>