<template>
  <div class="container mt-5">
    <div class="row mb-4 align-items-end">
      <!-- Dropdown for teams -->
      <div class="col-md-4">
        <div class="mb-3">
          <label for="teamSelect" class="form-label">Select a team:</label>
          <select class="form-select form-select-sm" v-model="selectedTeam"
            @change="fetchTestRuns(`/api/v1/teams/${this.selectedTeam}/test-runs/`)" id="teamSelect">
            <option disabled value="" selected>Please select a team</option>
            <option v-for="team in teams" :key="team.id" :value="team.id">{{ team.name }}</option>
          </select>
        </div>
      </div>

      <!-- Search Bar -->
      <div class="col-md-8">
        <div class="input-group">
          <input type="text" v-model="searchQuery" @input="handleQueryChange" class="form-control" placeholder="Search test runs...">
          <span class="input-group-text"><i class="fas fa-search"></i></span>
        </div>
      </div>
    </div>

    <!-- Display test runs -->
    <div v-for="testRun in testRuns" :key="testRun.id" class="card mb-3">
      <router-link :to="{ name: 'TestRunView', params:{ teamId: `${this.selectedTeam}`, testRunId:`${testRun.id}` } }" class="text-decoration-none">
        <div class="card-body">
          <h5 class="card-title">Test Run #{{ testRun.id }} - {{ testRun.name }}</h5>
          <div v-if="testRun.is_public" class="badge bg-success">Public</div>
          <div class="card-text mt-2">
            <div class="row">
              <div class="col-12 col-md-6" v-for="(attribute, index) in getFirstTwoAttributes(testRun.attributes)" :key="index">
                <strong>{{ attribute.key }}:</strong> {{ attribute.value || 'N/A' }}
              </div>
            </div>
            <div v-if="Object.keys(testRun.attributes).length > 2" class="collapse" :id="'collapseAttributes' + testRun.id">
              <div class="row">
                <div class="col-12 col-md-6" v-for="(attribute, index) in getRemainingAttributes(testRun.attributes)" :key="index">
                  <strong>{{ attribute.key }}:</strong> {{ attribute.value || 'N/A' }}
                </div>
              </div>
            </div>
            <button class="btn btn-link p-0" type="button" data-bs-toggle="collapse" :data-bs-target="'#collapseAttributes' + testRun.id" aria-expanded="false">
              Show more
            </button>
          </div>
          <p class="card-text text-muted small">Executed at: {{ new Date(testRun.executed_at).toLocaleDateString() }}</p>
        </div>
      </router-link>
    </div>

    <!-- Pagination -->
    <nav aria-label="Pagination" v-if="testRuns.length > 0">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ 'disabled': !previousPageUrl }">
          <a class="page-link" tabindex="-1" @click.prevent="fetchTestRuns(this.previousPageUrl)">Previous</a>
        </li>
        <li class="page-item" :class="{ 'disabled': !nextPageUrl }">
          <a class="page-link" @click.prevent="fetchTestRuns(this.nextPageUrl)">Next</a>
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
    toggleShowAllAttributes(testRun) {
      testRun.showAllAttributes = !testRun.showAllAttributes;
    },
  },
  computed: {
    getFirstTwoAttributes() {
      return (attributes) => {
        return Object.entries(attributes)
          .slice(0, 2)
          .map(([key, value]) => ({ key, value }));
      };
    },
    getRemainingAttributes() {
      return (attributes) => {
        return Object.entries(attributes)
          .slice(2)
          .map(([key, value]) => ({ key, value }));
      };
    },
  },
};
</script>

<style scoped>
/* Styling for the component */

/* Team selection dropdown and search bar */
.form-select-sm {
  max-width: 300px;
}

/* Test Run Cards */
.card {
  border: 1px solid #dcdcdc;
  transition: transform 0.1s ease-in-out;
}

.card:hover {
  transform: scale(1.02);
}

.card-body {
  position: relative;
}

.card-title {
  color: #333;
  font-weight: bold;
}

.badge {
  position: absolute;
  top: 20px;
  right: 20px;
}

/* Pagination styles */
.pagination .page-link {
  color: #3a6f8f;
  background-color: #e9f1fa;
  border-color: #dcdcdc;
}

.pagination .page-link:hover {
  background-color: #a3d5ff;
  border-color: #a3d5ff;
}

.pagination .disabled .page-link {
  color: #777;
  background-color: #e9ecef;
  border-color: #dcdcdc;
  cursor: not-allowed;
}

/* Small text style for less important info */
.small {
  font-size: 0.8rem;
}

/* Show more button for attributes */
.btn-link {
  font-size: 0.8rem;
  text-decoration: none;
}

.btn-link:hover {
  text-decoration: underline;
}
</style>