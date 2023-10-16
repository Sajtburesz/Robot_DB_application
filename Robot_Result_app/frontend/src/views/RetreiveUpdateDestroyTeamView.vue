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
            <div class="float-end">
    <!-- Button to open the search modal -->
    <button class="btn btn-custom-light-sky-blue" @click="showModal = true">+</button>
    <!-- Search Modal -->
    <div v-if="showModal" class="modal"> 
    <div class="modal-content">
        <span @click="closeModal" class="close">&times;</span>
        <UserSearchComponent v-on:set-users="setUsers" ></UserSearchComponent>
        <ul>
            <li v-for="user in querried_users" :key="user.username" >
                {{ user.username }}
                <span v-if="containsUsername(user.username)">User already in team</span>
                <button v-else type="button" @click="addMember(user.username)">Add Member</button>
            </li>
        </ul> 
        </div>
    </div>
</div>
           

            <!-- Members -->
            <div class="col-2 w-100 p-1 m-1" v-for="member in this.members" :key="member.id">
                <div class="d-flex justify-content-between align-items-center border-bottom pb-2 border-2">
                    <span>{{ member.username }}</span>
                    <button v-if="maintainer" class="btn btn-danger" @click="removeMember(member.username)">
                         Remove from team
                    </button>
                </div>
            </div>

        </div>
    </div>
</template>
  
<script>
import 'font-awesome/css/font-awesome.css'
import { axios } from "@/common/api.service.js";
import UserSearchComponent from "@/components/UserSearch.vue";

export default {
    components: {
        UserSearchComponent
    },
    data() {
        return {
            newTeamName: "",
            editingName: false,
            maintainer: true,

            showModal: false,

            querried_users: [],
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
        containsUsername(usernameToCheck) {
            return Object.values(this.members).some(member => member.username === usernameToCheck);
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
        },
        closeModal() {
            this.showModal = false;
            this.querried_users = [];
        },
        setUsers(userQuery){
            this.querried_users = userQuery;
        },
        async addMember(username) {
            let obj = { members: [] };
            obj.members.push(username);
            const response = await axios.put("/api/v1/teams/" + this.$route.params.teamId + "/add-members/", obj);
            this.members = response.data.members.map(member => {
                return {
                    username: member
                }
            });
        },
        async removeMember(username){
            let obj = { members: [] };
            obj.members.push(username);
            await axios.put("/api/v1/teams/" + this.$route.params.teamId + "/remove-members/", obj);
            this.members = this.members.filter(member => member.username !== username);
        }
    }
    // TODO: Handle response codes with a popup warning and make sure saved elements don't change
};
</script>
  
<style>
/* Styles for the modal (simple example) */
.modal {
  display: block;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.7);
}

.modal-content {
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 30%;
  background-color: #fefefe;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
}
</style>