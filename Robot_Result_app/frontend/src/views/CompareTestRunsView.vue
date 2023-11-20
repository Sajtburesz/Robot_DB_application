<template>
  <div class="container-fluid mt-5">
    <h2>Test Run Comparison</h2>
    <div class="row">
      <div class="col-md-6 border-end border-2">
        <h3>Test Run #{{ storedTestRuns[0].id }}</h3>
        <RetreiveTestRunComponent :testRunId="storedTestRuns[0].id" :teamId="storedWayOfAccess.includes(storedTestRuns[0].id) ? 'public' : storedTestRuns[0].team"/>
      </div>
      <div class="col-md-6">
        <h3>Test Run #{{ storedTestRuns[1].id }}</h3>
        <RetreiveTestRunComponent :testRunId="storedTestRuns[1].id" :teamId="storedWayOfAccess.includes(storedTestRuns[1].id) ? 'public' : storedTestRuns[1].team"/>
      </div>
    </div>
  </div>
</template>
  
<script>
import RetreiveTestRunComponent from "@/components/RetreiveTestRun.vue";

export default {

components: {
    RetreiveTestRunComponent,
},
computed: {
    storedTestRuns() {
        return this.$store.state.testRuns;
    },
    storedWayOfAccess() {
        return this.$store.state.wayOfAccess;
    }
},

};
</script>
  

  