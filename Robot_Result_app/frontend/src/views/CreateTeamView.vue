<template>
    <div class="vh-100 my-5">
        <div class="container">
            <div class="row">
                <!-- Left Side Menu -->
                <div class="col-md-2 border-end border-2">
                    <LeftSideTeamMenu />
                </div>

                <!-- Create Team Form -->
                <div class="col-md-10 d-flex align-items-center justify-content-center">
                    <form @submit.prevent="createTeam" class="w-100">
                        <div class="mb-3">
                            <label for="teamName" class="form-label fw-bold">Team Name</label>
                            <input type="text" class="form-control" id="teamName" v-model="teamName" required>
                        </div>
                        <div class="mb-3">
                            <label for="membersSelect" class="form-label fw-bold">Select Team Members</label>
                            <select multiple class="form-control" id="membersSelect" v-model="selectedMembers">
                                <option v-for="user in users" :key="user.username" :value="user.username">
                                    {{ user.username }}
                                </option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-ucla-blue fw-bold">Create</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import LeftSideTeamMenu from "@/components/LeftSideTeamMenu.vue";
import { axios } from "@/common/api.service.js";

export default {
    components: {
        LeftSideTeamMenu
    },
    data() {
        return {
            teamName: "",
            selectedMembers: [],
            users: [],
        };
    },
    async created() {
        try {
            let nextPageUrl = "/api/v1/users/";
            while (nextPageUrl) {
                const response = await axios.get(nextPageUrl);
                if (response.data.results && Array.isArray(response.data.results)) {
                    this.users = this.users.concat(response.data.results);
                    nextPageUrl = response.data.next; // Move to the next page if it exists
                } else {
                    console.error("Expected an array in 'results' but got:", response.data);
                    break; // Exit the loop if the expected data structure is not met
                }
            }
        } catch (error) {
            console.error("Error fetching users:", error);
        }
    },

    methods: {
        async createTeam() {
            try {
                const payload = {
                    name: this.teamName,
                    members: this.selectedMembers
                };
                const response = await axios.post('/api/v1/teams/create/', payload);
               
               if (response.status === 201) {
                    this.teamName = "";
                    this.selectedMembers = [];
                    console.log(response.data);
                } else {
                    console.log("ERROR");
                }

            } catch (error) {
                console.error("Error creating team:", error);
                // Handle the error, maybe show an error message to the user
            }
        }
    }
    };
</script>
  
  