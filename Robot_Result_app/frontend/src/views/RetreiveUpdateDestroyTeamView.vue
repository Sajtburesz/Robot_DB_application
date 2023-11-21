<template>
    <div class="container py-5">

        <div class="container-fluid">
            <div class="row">
                <!-- Left side: Team Name and Editing -->
                <div class="col-6 text-start">
                    <div v-if="!editingName && (owner || maintainer || isAdmin)" style="cursor: pointer;" @click="startEditingName">
                        <h1>
                            {{ team.name }}
                            <i class="fa fa-pencil fs-6" style="cursor: pointer;"
                                @click="startEditingName" aria-hidden="true"></i>
                        </h1>
                    </div>
                    <div v-else-if="!editingName">
                        <h1>
                            {{ team.name }}
                        </h1>
                    </div>
                    <div v-else>
                        <input type="text" v-model="newTeamName" class="form-control mb-2">
                        <button @click="updateTeamName" class="btn btn-custom-ucla-blue me-2">Edit</button>
                        <button @click="cancelEditingName" class="btn btn-secondary">Cancel</button>
                    </div>
                </div>

                <!-- Right side: Delete Team / Leave Team button -->
                <div class="col-6 text-end">
                    <button class="btn btn-danger" v-if="(owner || isAdmin)" @click="deleteTeam">Delete Team</button>
                    <button class="btn btn-danger" v-else @click="leaveTeam">Leave Team</button>
                </div>
            </div>
        </div>


        <!-- Members List -->
        <div class="mt-5">
            <h2 class="d-inline-block">Members</h2>
            <div class="float-end">
                <!-- Button to open the search modal -->
                <button class="btn btn-custom-light-sky-blue" v-if="(owner || maintainer || isAdmin)"
                    @click="showModal = true">+</button>
                <!-- Search Modal -->
                <div v-if="showModal" class="modal fade show d-block" tabindex="-1" role="dialog">
                    <div class="modal-dialog modal-xl">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Add Members</h5>
                                <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <!-- User Search Component -->
                                <div class="d-flex justify-content-center">
                                    <UserSearchComponent v-on:set-users="setUsers" v-on:set-loading="setLoading">
                                    </UserSearchComponent>
                                </div>
                                <div v-if="isLoading" class="d-flex justify-content-center my-4">
                                    <div class="spinner-border text-primary" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>
                                </div>
                                <!-- Users List Table -->
                                <table v-else class="table table-striped mt-3">
                                    <thead v-if="querried_users.length !== 0">
                                        <tr>
                                            <th>Username</th>
                                            <th>Status</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="user in querried_users" :key="user.username">
                                            <td>{{ user.username }}</td>
                                            <td v-if="containsUsername(user.username)">Member</td>
                                            <td v-else>-</td>
                                            <td>
                                                <button v-if="!containsUsername(user.username)" type="button"
                                                    class="btn btn-sm bg-ucla-blue clickable-item text-seasalt" @click="addMember(user.username)">Add
                                                    Member</button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>


            <div
                class="col-12 p-1 m-1 d-flex justify-content-between align-items-center border-bottom border-dark pb-2 border-2 bg-french-grey">
                <div class="col-4 d-flex justify-content-start">
                    <h5 class="fw-bold">User</h5>
                </div>
                <div class="col-4 d-flex justify-content-center">
                    <h5 class="fw-bold">Role</h5>
                </div>
                <div class="col-4"></div>
            </div>

            <div class="col-12 p-1 m-1" v-for="member in this.members" :key="member.id">
                <div class="d-flex justify-content-between align-items-center border-bottom pb-2 border-2">

                    <!-- First Part: Username -->
                    <div class="col-4 d-flex justify-content-start">
                        <span class="fw-bold">{{ member.username }}</span>
                    </div>
                    <!-- Second Part: Role -->
                    <div class="col-4 d-flex justify-content-center">
                        <div>
                            <div v-if="member.role !== 'Owner' && member.role !== 'Admin' && (owner || maintainer || isAdmin)">
                                <MemberRoleComponent :member="member" :roles="roles" @role-changed="handleRoleChange">
                                </MemberRoleComponent>
                            </div>
                            <span v-else>{{ member.role }}</span>
                        </div>
                    </div>

                    <!-- Third Part: Remove Button -->
                    <div class="col-4 d-flex justify-content-end">
                        <button
                            v-if="(maintainer || owner || isAdmin) && member.role != 'Owner' && member.role != 'Admin' && member.username !== this.currentUsername"
                            class="btn btn-danger ms-2" @click="removeMember(member.username)">
                            Remove from team
                        </button>
                    </div>

                </div>
            </div>


        </div>
    </div>
</template>
  
<script>
import 'font-awesome/css/font-awesome.css'
import { axios } from "@/common/api.service.js";

import UserSearchComponent from "@/components/UserSearch.vue";
import MemberRoleComponent from "@/components/MemberRole.vue";


export default {
    components: {
        UserSearchComponent,
        MemberRoleComponent
    },
    data() {
        return {
            newTeamName: "",
            editingName: false,
            isLoading: false,

            maintainer: false,
            owner: false,

            roles: ['Member', 'Maintainer'],

            showModal: false,

            querried_users: [],
            team: {},
            members: {},
            currentUsername: null,
        };
    },
    async created() {
        let teamId = this.$route.params.teamId;

        const response = await axios.get("/api/v1/teams/" + teamId + "/");

        this.members = response.data.members.map(member => {
            return {
                username: member.username,
                role: member.role
            }
        });
        
        const username = this.currentUser();
    
        if (response.data.owner === username) {
            this.owner = true;
        }
        this.maintainer = response.data.is_maintainer;
        this.team = response.data;

    },
    computed: {
        isAdmin() {
            this.$store.dispatch('fetchAdminStatus');
            return this.$store.state.isAdmin;
        },
    },
    methods: {
        async currentUser() {
            const username = await axios.get("/auth/users/me/");
            this.currentUsername = username.data.username;
            return username.data.username;
        },
        async handleRoleChange(payload) {
            const { member, newRole } = payload;

            let obj = { "username": "", "is_maintainer": false };
            let response = "";

            if (newRole == 'Maintainer') {
                obj.username = member.username;
                obj.is_maintainer = true;
                response = await axios.put("/api/v1/teams/" + this.$route.params.teamId + "/roles/", obj);
            } else {
                obj.username = member.username;
                obj.is_maintainer = false;
                response = await axios.put("/api/v1/teams/" + this.$route.params.teamId + "/roles/", obj);
            }

            if (response.status == "200") {
                const memberData = await axios.get("/api/v1/teams/" + this.$route.params.teamId + "/");
                this.members = [];
                this.members = memberData.data.members.map(member => {
                    return {
                        username: member.username,
                        role: member.role
                    }
                });
                this.maintainer = memberData.data.is_maintainer;
            }
            // TODO: ERROR Handling
        },
        containsUsername(usernameToCheck) {
            return Object.values(this.members).some(member => member.username === usernameToCheck);
        },
        startEditingName() {
            this.editingName = true;
            this.newTeamName = this.team.name;
        },
        async updateTeamName() {

            try {
                const response = await axios.put("/api/v1/teams/" + this.$route.params.teamId + "/", { name: this.newTeamName });

                this.team.name = response.data.name;
                this.editingName = false;
            } catch (error) {
                this.$toast.error('You do not have permission to access this resource.', {
                    duration: 4000,
                });
            }
        },
        cancelEditingName() {
            this.editingName = false;
        },
        closeModal() {
            this.showModal = false;
            this.querried_users = [];
        },
        setUsers(userQuery) {
            this.querried_users = userQuery;
        },
        setLoading(bool) {
            
            this.isLoading = bool;
        },
        async addMember(username) {
            let obj = { members: [] };
            obj.members.push(username);
            const response = await axios.put("/api/v1/teams/" + this.$route.params.teamId + "/add-members/", obj);

            if (response.status == "200") {
                const response = await axios.get("/api/v1/teams/" + this.$route.params.teamId + "/");
                this.members = [];
                this.members = response.data.members.map(member => {
                    return {
                        username: member.username,
                        role: member.role
                    }
                });
            }

        },
        async removeMember(username) {
            let obj = { members: [] };
            obj.members.push(username);
            await axios.put("/api/v1/teams/" + this.$route.params.teamId + "/remove-members/", obj);
            this.members = this.members.filter(member => member.username !== username);
        },
        async leaveTeam() {
            await axios.post("/api/v1/teams/" + this.$route.params.teamId + "/leave/");
            this.$router.push("/");
        },
        async deleteTeam() {
            await axios.delete("/api/v1/teams/" + this.$route.params.teamId + "/");
            this.$router.push("/");
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
    background-color: rgba(0, 0, 0, 0.7);
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

.btn-custom-outline-danger {
    color: red;
    background-color: #333;
    border: 2px solid red;
}

.btn-custom-outline-danger:hover {
    color: white;
    background-color: #740606;
    border: 2px solid white;
}
</style>