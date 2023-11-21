<template>
    <div class="container mt-5" :class="{ 'loading': isLoading }">

        <h1>Upload Test Run</h1>

        <form @submit.prevent="submitForm" class="mt-4">
            <!-- Team Selection -->
            <div class="col-md-12">
                <label for="team-dropdown" class="form-label text-ucla-blue">Team:</label>
                <div class="dropdown" ref="teamDropdown">
                    <button class="btn btn-secondary dropdown-toggle w-100 bg-ucla-blue text-seasalt truncate" type="button"
                            id="team-dropdown" data-bs-toggle="dropdown" aria-expanded="false" @click="toggleTeamDropdown()">
                        {{ selectedTeamName || 'Select a team' }}
                    </button>
                    <div class="dropdown-menu w-100" aria-labelledby="team-dropdown">
                        <div class="p-2">
                            <input type="text" class="form-control mb-2 bg-seasalt text-jet" v-model="teamFilter"
                                placeholder="Type to filter..." @input="filterTeams()">
                        </div>
                        <ul class="list-group overflow-auto" style="max-height: 200px;">
                            <li class="list-group-item bg-seasalt text-jet bg-animation clickable-item " href="#"
                                v-for="team in filteredTeams" :key="team.id" @click.prevent="selectTeam(team)">
                                {{ team.name }}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <!-- File Upload -->
            <div class="mb-3">
                <label for="outputFile" class="form-label">Upload TestRun XML:</label>
                <input type="file" id="outputFile" ref="fileInput" class="form-control" accept=".xml" required
                    @change="handleFileUpload" />
            </div>
            <!-- Attribute Fields -->
            <div v-for="attribute in attributes" :key="attribute.key_name" class="mb-3">
                <label :for="attribute.key_name" class="form-label">{{ attribute.key_name }}</label>
                <input v-model="formAttributes[attribute.key_name]" :name="attribute.key_name" :id="attribute.key_name" class="form-control" />
            </div>
            <!-- Is Public -->
            <div class="mb-3 form-check">
                <label class="form-check-label" for="public">Public Test Run</label>
                <input type="checkbox" class="form-check-input" id="public" v-model="is_public">
            </div>
            <button type="submit" class="btn bg-ucla-blue clickable-item text-seasalt" @click="createTestRun()">Upload Test Run</button>
        </form>
        <!-- Loading Indicator -->
        <div v-if="isLoading" class="loading-overlay">
            <div class="loading-spinner"></div>
        </div>
    </div>
</template>


<script>
import { axios } from "@/common/api.service.js";

export default {
    data() {
        return {
            teams: [],
            selectedTeam: null,
            selectedTeamName: null,
            teamFilter: '',
            filteredTeams: [],

            attributes: [],
            is_public: false,

            formAttributes: {},
            isLoading: false,
        };
    },
    async beforeCreate() {
        try {
            const attributes = await axios.get('/api/v1/attributes/');
            this.attributes = attributes.data.results;
            this.attributes.forEach(attribute => {
                this.formAttributes[attribute.key_name] = '';
            });
        } catch (error) {
            this.$toast.error(error.request.statusText, {
                duration: 4000,
            });
        }
    },
    async created() {
        try {
            const user = await axios.get('/auth/users/me/');
            let url = '/api/v1/users/' + user.data.username + '/teams/';
            let allTeams = [];
            while (url) {
                const response = await axios.get(url);
                allTeams = allTeams.concat(response.data.results.map(team => ({ id: team.id, name: team.name })));
                url = response.data.next;
            }
            this.teams = allTeams;
            this.filteredTeams = this.teams;
        

        } catch (error) {
            this.$toast.error(error.request.statusText, {
                duration: 4000,
            });
        }
    },

    methods: {
        handleFileUpload() {
            this.uploadedFile = this.$refs.fileInput.files[0];
        },

        async createTestRun() {
            this.isLoading = true;
            const formData = new FormData();

            formData.append('output_file', this.uploadedFile);
            formData.append('team', this.selectedTeam);
            formData.append('is_public', this.is_public ? 'True' : 'False');
            formData.append('attributes', JSON.stringify(this.formAttributes));
            
            try {
                const response = await axios.post('/api/v1/upload/', formData);
                this.$toast.success("Upload Successfull");
                this.$router.push({ name: 'TestRunView', params: { "teamId" : response.data.team, "testRunId":response.data.id } });
            } catch (error) {
                this.$toast.error(`Something went wrong during test run upload. Please check the uploaded file. Response Text: ${error.request.statusText}`, {
                    duration: 4000,
                });
                return;
            }finally{
                this.isLoading = false;
            }
        },
        filterTeams() {
        if (this.teamFilter) {
            this.filteredTeams = this.teams.filter((team) =>
                team.name.toLowerCase().includes(this.teamFilter.toLowerCase())
            );
        } else {
            this.filteredTeams = this.teams;
        }
        },
        selectTeam(team) {
            this.selectedTeam = team.id;
            this.selectedTeamName = team.name;
            this.teamFilter = '';
            this.filteredTeams = this.teams;
            this.$refs.teamDropdown.classList.remove('show');
            this.selectedTeamName = team.name;
        },
        toggleTeamDropdown() {
            this.$refs.teamDropdown.classList.toggle('show');
        },
    },
};
</script>

<style scoped>
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.7);
    z-index: 1000;
    display: flex;
    justify-content: center;
    align-items: center;
}

.loading-spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 2s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading {
    pointer-events: none;
    opacity: 0.5;
}
</style>