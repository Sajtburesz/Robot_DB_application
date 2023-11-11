<template>
    <div class="container mt-5">
        <h1>Create Test Run</h1>

        <form @submit.prevent="submitForm" class="mt-4">
            <!-- Team Selection -->
            <div class="mb-3">
                <label class="form-label">Team:</label>
                <select v-model="selectedTeam" class="form-select" required>
                    <option v-for="team in teams" :key="team.id" :value="team.id">{{ team.name }}</option>
                </select>
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
            <button type="submit" class="btn btn-primary" @click="createTestRun()">Create Test Run</button>
        </form>
    </div>
</template>


<script>
import { axios } from "@/common/api.service.js";

export default {
    data() {
        return {
            teams: [],

            attributes: [],
            is_public: null,

            selectedTeam: null,
            formAttributes: {},
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

            const teams = await axios.get('/api/v1/users/' + user + '/teams/');
            this.teams = teams.data.results;

        } catch (error) {
            this.$toast.error(error.request.statusText, {
                duration: 4000,
            });
        }
    },
    watch: {
  is_public(newValue) {
    console.log('is_public changed to:', newValue);
  },
},
    methods: {
        handleFileUpload() {
            this.uploadedFile = this.$refs.fileInput.files[0];
        },

        async createTestRun() {
            const formData = new FormData();

            formData.append('output_file', this.uploadedFile);
            formData.append('team', this.selectedTeam);
            formData.append('is_public', this.is_public);
            formData.append('attributes', JSON.stringify(this.formAttributes));
            
            try {
                await axios.post('/api/v1/upload/', formData);

            } catch (error) {
                this.$toast.error(error.request.statusText, {
                    duration: 4000,
                });
                return;
            }
            this.$toast.success("Upload Successfull")
        },
    },
};
</script>
  