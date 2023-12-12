<template>
  <div class="vh-100">
    <!-- Main Content Section -->
    <div class="container mt-4">
      <div class="card mb-4 h-100">
        <div class="detailes-header d-flex justify-content-between align-items-center ps-2 pe-3">
          <span>{{ `#${testRun.id}` }} Test Run Details</span>
          <div>
            <span class="badge" :class="`badge-${testRun.status === 'FAIL' ? 'danger' : 'success'}`">{{ testRun.status
            }}</span>
            <button class="btn btn-link ms-2" id="testrundetails" @click="showTestRunDetails = !showTestRunDetails">
              <font-awesome-icon
                :icon="showTestRunDetails ? 'fa-solid fa-circle-arrow-up' : 'fa-solid fa-circle-arrow-down'" />
            </button>
          </div>
        </div>
        <div v-if="showTestRunDetails" class="card-body">
          <div class="mb-3">
            <div class="d-flex justify-content-between align-items-center">
              <span><strong>Executed At:</strong> {{ new Date(testRun.executed_at).toLocaleString() }}</span>
              <div>
                <button id="editbutton" v-if="isNotPublic && (this.role !== 'Member' || isAdmin)" class="btn bg-ucla-blue clickable-item text-seasalt btn-sm me-2"
                  @click="toggleEditMode">{{ editMode ? 'Save' : 'Edit'
                  }}</button>
                <button v-if="editMode && isNotPublic && (this.role !== 'Member' || isAdmin)" class="btn btn-secondary btn-sm me-2"
                  @click="cancelEdit">Cancel</button>
                <button v-if="isNotPublic && (this.role !== 'Member' || isAdmin)" class="btn btn-danger btn-sm" @click.prevent data-bs-toggle="modal"
                  data-bs-target="#testRunDeleteModal">
                  <font-awesome-icon icon="fa-solid fa-trash" />
                </button>
              </div>
            </div>
          </div>
          <div v-if="editMode" class="form-check form-switch mb-3">
            <input id='public_testrun' class="form-check-input" type="checkbox" v-model="testRun.is_public">
            <label class="form-check-label" for="flexSwitchCheckChecked">Public</label>
          </div>
          <div v-else>
            <p v-if="testRun.is_public" ><strong>Public Testrun</strong></p>
          </div>
          <ul class="list-group mb-3">
            <li v-for="(value, key) in testRun.attributes" :key="key" class="list-group-item">
              <strong>{{ key }}:</strong>
              <span v-if="!editMode">{{ value || 'None' }}</span>
              <input v-else type="text" class="form-control" v-model="testRun.attributes[key]">
            </li>
          </ul>
        </div>
      </div>

      <!-- Delete Confirmation Modal -->
      <div class="modal fade" tabindex="-1" role="dialog" aria-hidden="true" id="testRunDeleteModal">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Delete Test Run</h5>
              <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <p>Are you sure about deleting this Test Run?</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
              <button type="button" class="btn btn-danger" @click="deleteTestRun()" data-bs-dismiss="modal">Yes</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Suites List -->
      <div v-for="suite in suites" :key="suite.id" class="card mb-4">
        <div class="card-header d-flex justify-content-between align-items-center">
          <button class="btn btn-link text-start w-100 p-0 text-decoration-none text-dark"
            @click="toggleSuiteDetails(suite.id)">
            <div class="d-flex justify-content-between align-items-center">
              <span>{{ suite.name }}</span>
              <div class="d-flex align-items-center">
                <span class="badge" :class="`badge-${suite.status === 'FAIL' ? 'danger' : 'success'}`">{{ suite.status
                }}</span>
                <font-awesome-icon class="btn btn-link ms-2"
                  :icon="expandedSuites.includes(suite.id) ? 'fa-solid fa-circle-arrow-up' : 'fa-solid fa-circle-arrow-down'" />
              </div>
            </div>
          </button>
        </div>
        <div v-if="expandedSuites.includes(suite.id)" class="card-body">
          <div v-for="testCase in currentSuiteDetails[suite.id]?.test_cases" :key="testCase.id"
            class="mb-2 border-bottom border-2 pb-2">
            <div v-if="testCase.status === 'PASS'">
              <span class="me-2">{{ testCase.name }}</span>
              <span class="badge" :class="`badge-${testCase.status === 'FAIL' ? 'danger' : 'success'}`">{{ testCase.status
              }}</span>
            </div>
            <div v-else @click="toggleTestCaseDetails(suite.id, testCase.id)"
              class="d-flex justify-content-between align-items-center cursor-pointer">
              <div>
                <span class="me-2">{{ testCase.name }}</span>
                <span class="badge" :class="`badge-${testCase.status === 'FAIL' ? 'danger' : 'success'}`">{{
                  testCase.status }}</span>
              </div>
              <font-awesome-icon class="btn btn-link"
                :icon="this.expandedTestCases.includes(testCase.id) ? 'fa-solid fa-circle-arrow-up' : 'fa-solid fa-circle-arrow-down'" />
            </div>
            <div v-if="expandedTestCases.includes(testCase.id)" class="mt-2 keyword-detailes">
              <p class="fw-bold">Failed Keywords:</p>
              <div v-for="keyword in currentTestCaseDetails[testCase.id]?.keywords" :key="keyword.id"
                class="mb-2 border-top border-2 pt-2 ps-3">
                <h6 class="fw-bold">{{ keyword.name }}</h6>
                <div v-if="keyword.log_message.length > 2" class="ps-3">
                  <p v-for="(line, index) in cleanResponse(keyword.log_message)" :key="index" class="message-text">{{ line
                  }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination Section -->
      <nav aria-label="Suite pagination">
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ 'disabled': !prevSuitesUrl }">
            <button class="page-link" @click="loadTestRun(this.prevSuitesUrl)"
              :disabled="!prevSuitesUrl">Previous</button>
          </li>
          <li class="page-item" :class="{ 'disabled': !nextSuitesUrl }">
            <button class="page-link" @click="loadTestRun(this.nextSuitesUrl)" :disabled="!nextSuitesUrl">Next</button>
          </li>
        </ul>
      </nav>
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
      role: null,
      showTestRunDetails: false,
      editMode: false,
      showDeleteConfirmation: false,

      nextSuitesUrl: null,
      prevSuitesUrl: null
    };
  },
  created() {
    this.loadTestRun(`/api/v1/teams/${this.teamId}/test-runs/${this.testRunId}/`);
  },
  computed: {
    isNotPublic() {
      return this.teamId !== 'public';
    },
    isAdmin() {
      this.$store.dispatch('fetchAdminStatus');
      return this.$store.state.isAdmin;
    },
  },
  methods: {
    toggleEditMode() {
      if (this.editMode) {
        this.saveTestRunDetails(); // Save the changes
      } else {
        this.originalTestRun = JSON.parse(JSON.stringify(this.testRun)); // Copy original data
      }
      this.editMode = !this.editMode;
    },
    async fetchRole() {
      try {
        const response = await axios.get("/api/v1/teams/" + this.teamId + "/");
        const username = await axios.get("/auth/users/me/");

        const foundMember = response.data.members.find(member => member.username === username.data.username);

        if (response.data.owner === username.data.username) {
          this.role = 'owner';
        } else {
          this.role = foundMember.role;
        }
      } catch (error) {
        this.$toast.error('Error fetching user role.');
      }

    },
    cancelEdit() {
      this.testRun = JSON.parse(JSON.stringify(this.originalTestRun)); // Revert changes
      this.originalTestRun = null;
      this.editMode = false;
    },
    extractPath(url) {
      if (!url) return null;
      const basePath = '/api/v1/';
      const index = url.indexOf(basePath);
      return index !== -1 ? url.substring(index) : null;
    },
    async saveTestRunDetails() {
      try {
        await axios.put(`/api/v1/teams/${this.teamId}/test-runs/${this.testRunId}/`, this.testRun);
      } catch (error) {
        this.$toast.error(`Error updating testrun details.`);
      }
    },
    async deleteTestRun() {
      try {
        await axios.delete(`/api/v1/teams/${this.teamId}/test-runs/${this.testRunId}/`);
        this.$router.push({ name: 'ListTestRunsView' });
      } catch (error) {
        this.$toast.error(`Error during deleting testrun.`);
      }
    },
    async loadTestRun(url) {
      try {
        const response = await axios.get(url);
        this.testRun = response.data;
        this.suites = this.testRun.suites.suites;
        this.nextSuitesUrl = this.extractPath(response.data.suites.next);
        this.prevSuitesUrl = this.extractPath(response.data.suites.previous);
        if (this.teamId !== 'public'){
          this.fetchRole();
        }
      } catch (error) {
        this.$toast.error(`Error fetching test run.`);
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
          (response.data);
          this.currentSuiteDetails[suiteId] = response.data;
        } catch (error) {
          this.$toast.error(`Error fetching suite details.`);
        }
      }
    },
    toggleTestCaseDetails(suiteId, testCaseId) {
      const index = this.expandedTestCases.indexOf(testCaseId);
      if (index === -1) {
        this.expandedTestCases.push(testCaseId);
        this.loadTestCaseDetails(suiteId, testCaseId);
      } else {
        this.expandedTestCases.splice(index, 1);
      }
    },
    async loadTestCaseDetails(suiteId, testCaseId) {
      if (!this.currentTestCaseDetails[testCaseId]) {
        try {
          const response = await axios.get(`/api/v1/teams/${this.teamId}/test-runs/${this.testRunId}/${suiteId}/${testCaseId}/`);
          (response.data);
          this.currentTestCaseDetails[testCaseId] = response.data;
        } catch (error) {
          this.$toast.error(`Error fetching test case details.`);
        }
      }
    },
    cleanResponse(inputText) {
      let text = inputText;

      if (text.startsWith('[')) {
        text = text.substring(1);
      }
      if (text.endsWith(']')) {
        text = text.substring(0, text.length - 1);
      }

      text = text.replace(/,|'/g, '');

      return text.split(/\\n/g);
    },
  }
};
</script>

<style scoped>
.card-header {
  background-color: #e9f1fa;
  font-weight: bold;
}

.detailes-header {
  background-color: #B4BBC2;
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
  overflow-wrap: break-word;
  word-wrap: break-word;
  white-space: pre-wrap;
}

.list-group-item {
  background-color: #f7f7f7;
  border: 1px solid #dcdcdc;
  word-wrap: break-word;
  max-width: 100%;
}

.comments-section {
  width: 300px;
  /* Adjust the width as needed */
  height: calc(100vh - 56px);
  /* Adjust the height as needed, 56px for navbar if present */
}

.keyword-details {
  max-width: 100%;
  /* Ensures it doesn't overflow */
}

.keyword-details>* {
  word-wrap: break-word;
  /* Wraps text to prevent horizontal overflow */
}</style>
 