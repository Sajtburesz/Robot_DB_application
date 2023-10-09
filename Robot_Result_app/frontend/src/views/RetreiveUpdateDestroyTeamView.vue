<template>
    <div class="container py-5">

        <!-- Team Name Section -->
        <div v-if="!editingName" @click="startEditingName">
            <h1>{{ team.name }} <i class="fa fa-pencil fs-6" aria-hidden="true"></i></h1>
        </div>
        <div v-else>
            <input type="text" v-model="newTeamName" class="form-control mb-2">
            <button @click="updateTeamName" class="btn btn-custom-ucla-blue me-2">Edit</button>
            <button @click="cancelEditingName" class="btn btn-secondary">Cancel</button>
        </div>


        <!-- Members List -->
        <div class="mt-5">
            <h2 class="d-inline-block">Members</h2>
            <button class="btn btn-custom-light-sky-blue float-end" @click="showAddMember = !showAddMember">+</button>

            <!-- Add Member Form -->
            <div v-if="showAddMember">
                <!-- Your form to add members goes here -->
            </div>

            <!-- Members -->
            <div class="card" v-for="member in this.members" :key="member.id" @click="toggleMemberDetails(member)">
                {{ member.username }}
                <div v-if="member.showDetails">
                    <button class="btn btn-danger">Remove from team</button>
                </div>
            </div>
        </div>

    </div>
</template>
  
<script>
import 'font-awesome/css/font-awesome.css'
import { axios } from "@/common/api.service.js";
export default {
    data() {
        return {
            newTeamName: "",
            editingName: false,
            showAddMember: false,

            team: {},
            members: {},
        };
    },
    async created() {
        let teamId = this.$route.params.teamId;

        const response = await axios.get("/api/v1/teams/" + teamId + "/");

        this.members = response.data.members.map(member => {
            return {
                username: member,
                showDetails: false
            }
        });

        this.team = response.data;
    },
    methods: {
        toggleMemberDetails(member) {
            member.showDetails = !member.showDetails;
        },
        startEditingName() {
            this.editingName = true;
            this.newTeamName = this.team.name;  // Initialize the new name with the current name
        },
        updateTeamName() {
            // Your logic to update the team name goes here
            this.teamName = this.newTeamName;  // For now, just assign the new name
            this.editingName = false;
        },
        cancelEditingName() {
            this.editingName = false;
        }
    }
};
</script>
  