<template>
  <div class="container mt-5">
    <!-- Dropdown for teams -->
    <label for="teamSelect">Select a team</label>
    <select class="form-select" v-model="selectedTeam"
      @change="fetchTestRuns(`/api/v1/teams/${this.selectedTeam}/test-runs/`)" id="teamSelect">
      <option disabled value="Please select a team">Please select a team</option>
      <option v-for="team in teams" :key="team.id" :value="team.id">{{ team.name }}</option>
    </select>

    <!-- Search Bar -->
    <div class="mb-4"  v-if="testRuns.length != 0">
      <div class="input-group">
        <input type="text" v-model="searchQuery" @input="handleQueryChange" class="form-control" placeholder="Search...">
      </div>
    </div>


    <!-- Display test runs -->
    <div v-for="testRun in testRuns" :key="testRun.id" class="card mb-4 mt-2">
      <router-link :to="{ name: 'TestRunView', params:{teamId: `${this.selectedTeam}`, testRunId:`${testRun.id}`} }">
        <div class="card-body">
          <h5 class="card-title">Attributes:</h5>
          <div class="row">
            <div v-for="(value, key) in testRun.attributes" :key="key" class="col-6">
              <strong>{{ key }}</strong>: {{ value || 'N/A' }}
            </div>
          </div>
        </div>
      </router-link>
    </div>
    <!-- Pagination -->
    <nav>
      <ul class="pagination" v-if="testRuns.length != 0">
        <li class="page-item" :class="{ 'disabled': !previousPageUrl }">
          <a class="page-link btn" tabindex="-1" @click.prevent="fetchTestRuns(this.previousPageUrl)">Previous</a>
        </li>
        <li class="page-item" :class="{ 'disabled': !nextPageUrl }">
          <a class="page-link btn" @click.prevent="fetchTestRuns(this.nextPageUrl)">Next</a>
        </li>
      </ul>
    </nav>


  </div>
</template>

<script>
import { axios } from "@/common/api.service.js";

export default {
  data() {
    return {
      teams: [],
      selectedTeam: null,
      testRuns: [],

      nextPageUrl: null,
      previousPageUrl: null,

      searchQuery: "",
      debounceTimer: null
    };
  },
  created() {
    this.fetchTeams();
  },
  methods: {
    async fetchTeams() {
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
      } catch (error) {
        this.$toast.error("Error during fetching teams.");
      }
    },
    async fetchTestRuns(url) {
      try {
        const response = await axios.get(url);
        this.nextPageUrl = response.data.next;
        this.previousPageUrl = response.data.previous;
        this.testRuns = response.data.results;
        console.log(response.data.results);
      } catch (error) {
        this.$toast.error("Error during fetching test runs.");
      }
    },

    handleQueryChange() {
      clearTimeout(this.debounceTimer);

      this.debounceTimer = setTimeout(() => {
        const url = this.createQueryUrl();
        this.fetchTestRuns(url);
      }, 500);
    },
    createQueryUrl() {
      let url = `/api/v1/teams/${this.selectedTeam}/test-runs/?`;
      const params = this.searchQuery.replace(/\s+/g, '');
      url += params;
      
      return url;
    },
  }
};
</script>
