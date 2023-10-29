<template>
    <div class="container mt-5">
      <!-- Dropdown for teams -->
      <select class="form-select" v-model="selectedTeam" @change="fetchTestRuns">
        <option disabled value="">Please select a team</option>
        <option v-for="team in teams" :key="team.id" :value="team.id">{{ team.name }}</option>
      </select>
  
      <!-- Display test runs -->
      <ul class="list-group mt-4">
        <li v-for="testRun in testRuns" :key="testRun.id" class="list-group-item">{{ testRun.name }}</li>
      </ul>
  
      <!-- Pagination -->
      <nav class="mt-4">
        <ul class="pagination">
          <li class="page-item" :class="{ 'disabled': currentPage <= 1 }">
            <button class="page-link" @click="previousPage">Previous</button>
          </li>
          <li class="page-item" :class="{ 'disabled': testRuns.length < pageSize }">
            <button class="page-link" @click="nextPage">Next</button>
          </li>
        </ul>
      </nav>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        teams: [],
        selectedTeam: null,
        testRuns: [],
        currentPage: 1,
      };
    },
    created() {
      this.fetchTeams();
    },
    methods: {
      async fetchTeams() {
        try {
          const response = await axios.get('/api/users/teams/');
          this.teams = response.data;
        } catch (error) {
          console.error("Error fetching teams:", error);
        }
      },
      async fetchTestRuns() {
        try {
          const response = await axios.get(`/api/robot_test_management/teams/${this.selectedTeam}/test-runs/?page=${this.currentPage}`);
          this.testRuns = response.data;
        } catch (error) {
          console.error("Error fetching test runs:", error);
        }
      },
      nextPage() {
        this.currentPage++;
        this.fetchTestRuns();
      },
      previousPage() {
        this.currentPage--;
        this.fetchTestRuns();
      }
    }
  };
  </script>
  