<template>
  <div class="container mt-5">
    <div class="row mb-4">
      <!-- Dropdown for teams -->
      <div class="col-md-4 d-flex align-items-center">
        <div class="w-100 form-floating">
          <select class="form-select form-select-sm" v-model="selectedTeam"
            @change="fetchTestRuns(`/api/v1/teams/${this.selectedTeam}/test-runs/`)" id="teamSelect">
            <option v-for="team in teams" :key="team.id" :value="team.id">{{ team.name }}</option>
          </select>
          <label for="floatingSelect">Select a Team</label>
        </div>
      </div>

      <!-- Search Bar -->
      <div class="col-md-8 d-flex align-items-center">
        <div class="input-group w-100">
          <input type="text" v-model="searchQuery" @input="handleQueryChange" class="form-control" placeholder="Filter test runs...">
          <span class="input-group-text"><font-awesome-icon icon="fa-solid fa-magnifying-glass" /></span> 
        </div>
      </div>
    </div>

    <!-- Selection Summary -->
    <div v-if="selectedTestRuns.length > 0" class="mb-3 d-flex justify-content-between align-items-center">
      <span>
        Selected for compare ({{ selectedTestRuns.length}}/2): {{ selectedTestRuns.map(testRun => testRun.id).join(', ') }}
      </span>
      <div>
        <button v-if="selectedTestRuns.length === 2" class="btn btn-primary btn-sm" @click="compareTestRuns">Compare</button>
        <font-awesome-icon v-if="selectedTestRuns.length > 0"  class="btn btn-link hover-zoom-icon" @click="deleteSelectedTestruns()" icon="fa-solid fa-xmark" />
      </div>
    </div>

    <!-- Display test runs -->
    <div v-for="testRun in testRuns" :key="testRun.id" class="card mb-3">
      <div class="form-check ms-2 mt-2">
      <input class="form-check-input me-2" id="compareCheckbox" type="checkbox" v-model="selectedTestRuns" :value="testRun" @change="selectTestRun(testRun)">
      <label for="compareCheckbox" class="form-check-label text-muted">Add to compare</label>
    </div>
      <router-link :to="{ name: 'TestRunView', params:{ teamId: `${this.selectedTeam}`, testRunId:`${testRun.id}` } }" class="text-decoration-none">
        <div class="card-body">
          <h5 class="card-title">Test Run #{{ testRun.id }} - {{ testRun.name }}</h5>
          <div v-if="testRun.is_public" class="badge bg-success">Public</div>
          <div class="card-text mt-2">
          <div class="row">
            <div class="col-12 col-md-6" v-for="(value, key) in firstTwoAttributes(testRun.attributes)" :key="key">
              <strong>{{ key }}:</strong> {{ value || 'None' }}
            </div>
          </div>
          <div v-if="Object.keys(testRun.attributes).length > 2">
            <div v-if="testRun.showAllAttributes" class="row mt-2">
              <div class="col-12 col-md-6" v-for="(value, key) in remainingAttributes(testRun.attributes)" :key="key">
                <strong>{{ key }}:</strong> {{ value || 'None' }}
              </div>
            </div>
            <button class="btn btn-link p-0" type="button" @click.prevent="toggleShowAllAttributes(testRun)">
              {{ testRun.showAllAttributes ? 'Show less' : 'Show more' }}
            </button>
          </div>
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
      debounceTimer: null,
      selectedTestRuns: [],
      wayOfAccess: []
    };
  },
  created() {
    this.fetchTeams();
    this.fetchStoredTestRuns();
  },
  computed: {
    storedTestRuns() {
      return this.$store.state.testRuns;
    }
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

        this.teams.unshift({id:"public",name:"public"});
        this.selectedTeam = this.teams[0].id;
      
        await this.fetchTestRuns(`/api/v1/teams/${this.selectedTeam}/test-runs/`);
      } catch (error) {
        console.error("Error during fetching teams:", error);
      }
    },
    async fetchTestRuns(url) {
      try {
        const response = await axios.get(url);
        this.testRuns = response.data.results.map(tr => ({ ...tr, showAllAttributes: false }));
        this.nextPageUrl = response.data.next;
        this.previousPageUrl = response.data.previous;
        console.log(response.data.results);
      } catch (error) {
        console.error("Error during fetching test runs:", error);
      }
    },
    handleQueryChange() {
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => {
        this.fetchTestRuns(`/api/v1/teams/${this.selectedTeam}/test-runs/?search=&${this.searchQuery}`);
      }, 500);
    },
    toggleShowAllAttributes(testRun) {
      testRun.showAllAttributes = !testRun.showAllAttributes;
    },
    firstTwoAttributes(attributes) {
      return Object.entries(attributes).slice(0, 2).reduce((acc, [key, value]) => ({ ...acc, [key]: value }), {});
    },
    remainingAttributes(attributes) {
      return Object.entries(attributes).slice(2).reduce((acc, [key, value]) => ({ ...acc, [key]: value }), {});
    },

    selectTestRun(testRun) {
      if (this.selectedTestRuns.length > 2) {
        this.selectedTestRuns.pop(testRun);
        this.$toast.error("Only 2 Testruns can be selected");
      }

      if (this.selectedTeam === 'public') {
        if (this.wayOfAccess.includes(testRun.id)){
          this.wayOfAccess = this.wayOfAccess.filter(item => item !== testRun.id);
          this.$store.dispatch('setWayOfAccess', []);
          this.$store.dispatch('setWayOfAccess', this.wayOfAccess);
        }else {
          this.wayOfAccess.push(testRun.id);
          this.$store.dispatch('setWayOfAccess', []);
          this.$store.dispatch('setWayOfAccess', this.wayOfAccess);
        }
      }
      this.$store.dispatch('setTestRuns', []);
      this.$store.dispatch('setTestRuns', this.selectedTestRuns);
    },
    compareTestRuns() {
      this.$router.push({ name: 'CompareTestRunView' });
    },
    fetchStoredTestRuns(){
      this.storedTestRuns.map(testrun => this.selectedTestRuns.push(testrun));
    },
    deleteSelectedTestruns(){
      this.selectedTestRuns = [];
      this.$store.dispatch('setTestRuns', []);
    }
  }
};
</script>

<style scoped>

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

.hover-zoom-icon {
    transition: transform 0.3s ease;
}

.hover-zoom-icon:hover {
    transform: scale(1.1);
}
</style>