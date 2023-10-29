<template>
    <div class="container mt-4">
  
      <!-- Test Run Details -->
      <div class="card mb-4">
        <div class="card-header">
          Test Run Details
        </div>
        <div class="card-body">
          <h5 class="card-title">{{ testRun.attributes }}</h5>
        </div>
      </div>
  
      <!-- Suites List -->
      <div v-for="suite in suites" :key="suite.id" class="card mb-4">
        <div class="card-header">
          <button class="btn btn-link text-start w-100" @click="toggleSuiteDetails(suite.id)">
            {{ suite.name }}
          </button>
        </div>
  
        <!-- Suite Details (Lazy Loaded) -->
        <div v-if="expandedSuites.includes(suite.id)" class="card-body">
          <h6 class="mb-3">{{ currentSuiteDetails[suite.id]?.name }}</h6>
  
          <!-- Test Cases List -->
          <div v-for="testCase in currentSuiteDetails[suite.id]?.test_cases" :key="testCase.id">
            <button class="btn btn-outline-primary btn-sm d-block mt-2" @click="toggleTestCaseDetails(suite.id,testCase.id)">
              {{ testCase.name }}
            </button>
  
            <!-- Test Case Details (Lazy Loaded) -->
            <div v-if="expandedTestCases.includes(testCase.id)" class="mt-2">
              <h6 class="mb-2">{{ currentTestCaseDetails[testCase.id]?.name }}</h6>
              <p>{{ currentTestCaseDetails[testCase.id]?.description }}</p>
  
              <!-- Keywords List -->
              <ul class="list-group">
                <li v-for="keyword in currentTestCaseDetails[testCase.id]?.keywords" :key="keyword.id" class="list-group-item">
                  {{ keyword.name }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { axios } from "@/common/api.service.js";
  
  export default {
    props: ['testRunId', 'teamId'],
    data() {
      return {
        testRun: {},
        suites: [],
        expandedSuites: [],
        currentSuiteDetails: {},
        expandedTestCases: [],
        currentTestCaseDetails: {}
      };
    },
    created() {
      this.loadTestRun();
    },
    methods: {
      async loadTestRun() {
        try {
          const response = await axios.get(`/api/v1/teams/${this.teamId}/test-runs/${this.testRunId}/`);
          this.testRun = response.data;
          this.suites = this.testRun.suites.suites;
        } catch (error) {
          console.error("Error fetching test run:", error);
        }
      },
      toggleSuiteDetails(suiteId) {
        const index = this.expandedSuites.indexOf(suiteId);
        if (index === -1) {
          this.expandedSuites.push(suiteId);
          this.loadSuiteDetails(suiteId);
        } else {
          this.expandedSuites.splice(index, 1);
        }
      },
      async loadSuiteDetails(suiteId) {
        if (!this.currentSuiteDetails[suiteId]) {
          try {
            const response = await axios.get(`/api/v1/teams/${this.teamId}/test-runs/${this.testRunId}/${suiteId}/`);
            this.currentSuiteDetails[suiteId] = response.data;
          } catch (error) {
            console.error("Error fetching suite details:", error);
          }
        }
      },
      toggleTestCaseDetails(suiteId,testCaseId) {
        const index = this.expandedTestCases.indexOf(testCaseId);
        if (index === -1) {
          this.expandedTestCases.push(testCaseId);
          this.loadTestCaseDetails(suiteId,testCaseId);
        } else {
          this.expandedTestCases.splice(index, 1);
        }
      },
      async loadTestCaseDetails(suiteId,testCaseId) {
        if (!this.currentTestCaseDetails[testCaseId]) {
          try {
            const response = await axios.get(`/api/v1/teams/${this.teamId}/test-runs/${this.testRunId}/${suiteId}/${testCaseId}/`);
            console.log(response.data);
            this.currentTestCaseDetails[testCaseId] = response.data;
          } catch (error) {
            console.error("Error fetching test case details:", error);
          }
        }
      }
    }
  };
  </script>
  