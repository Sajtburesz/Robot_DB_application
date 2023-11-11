<template>
  <div class="container mt-4">
    <!-- Test Run Details -->
    <div class="card mb-4">
      <div class="card-header d-flex justify-content-between align-items-center">
        <span>Test Run Details</span>
        <button class="btn btn-link" @click="showTestRunDetails = !showTestRunDetails">
          {{ showTestRunDetails ? 'Hide' : 'Show' }}
        </button>
      </div>
      <div v-if="showTestRunDetails" class="card-body">
        <ul class="list-group mb-3">
          <li v-for="(value, key) in testRun.attributes" :key="key" class="list-group-item">
            <strong>{{ key }}:</strong> {{ value || 'None' }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Suites List -->
    <div v-for="suite in suites" :key="suite.id" class="card mb-4">
      <div class="card-header d-flex justify-content-between align-items-center">
        <!-- Entire header is clickable -->
        <button class="btn btn-link text-start w-100 p-0 text-decoration-none text-dark" @click="toggleSuiteDetails(suite.id)">
          <div class="d-flex justify-content-between align-items-center">
            <span>{{ suite.name }}</span>
            <span class="badge" :class="`badge-${suite.status === 'FAIL' ? 'danger' : 'success'}`">{{ suite.status }}</span>
          </div>
        </button>
      </div>
      <!-- Suite Details (Lazy Loaded) -->
      <div v-if="expandedSuites.includes(suite.id)" class="card-body">
        <h6 class="mb-3">Test Cases:</h6>
        <div v-for="testCase in currentSuiteDetails[suite.id]?.test_cases" :key="testCase.id" class="mb-2">
          <div @click="toggleTestCaseDetails(suite.id, testCase.id)" class="cursor-pointer">
            <span class="me-2">{{ testCase.name }}</span>
            <span class="badge" :class="`badge-${testCase.status === 'FAIL' ? 'danger' : 'success'}`">{{ testCase.status }}</span>
          </div>

          <!-- Test Case Details (Lazy Loaded) -->
          <div v-if="expandedTestCases.includes(testCase.id)" class="mt-2">
            <p>{{ currentTestCaseDetails[testCase.id]?.description }}</p>

            <!-- Keywords List -->
            <div v-for="keyword in currentTestCaseDetails[testCase.id]?.keywords" :key="keyword.id" class="mb-2">
              <h6>{{ keyword.name }}</h6>
              <p v-for="message in keyword.log_message" :key="message" class="message-text">{{ message }}</p>
            </div>
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
        currentTestCaseDetails: {},

        showTestRunDetails: false,
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
          console.log(response.data);
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
            console.log(response.data);
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

 <style scoped>
 .card-header {
   background-color: #e9f1fa;
   font-weight: bold;
 }
 
 .cursor-pointer {
   cursor: pointer;
 }
 
 .badge-danger {
   background-color: #dc3545;
 }
 
 .badge-success {
   background-color: #28a745;
 }
 
 .message-text {
   background-color: #f8f9fa;
   border-left: 3px solid #dcdcdc;
   padding: 5px;
   margin-bottom: 5px;
   white-space: pre-wrap; /* Ensure multi-line messages are displayed properly */
 }
 
 .list-group-item {
   background-color: #f7f7f7;
   border: 1px solid #dcdcdc;
 }
 
 /* Additional styles for modern look */
 </style>
 