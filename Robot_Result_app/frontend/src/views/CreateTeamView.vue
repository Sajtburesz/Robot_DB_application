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
                        <button type="submit" class="btn bg-ucla-blue clickable-item text-seasalt fw-bold">Create</button>
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
        };
    },

    methods: {
        async createTeam() {
            try {
                const payload = {
                    name: this.teamName,
                };
                const response = await axios.post('/api/v1/teams/create/', payload);
               

                let teamId = response.data.id;
                this.$router.push('/manage-team/' + teamId + '/');
                
            } catch (error) {
                if (error.response.data.detail){
                    this.$toast.error(`${error.response.data.detail}`);

                }else{
                    this.$toast.error(`Error creating team.`);
                }
            }
        }
    }
    };
</script>
  
  