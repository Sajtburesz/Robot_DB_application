<template>
    <div class="container mt-5">
      <h2>Test Run Comparison</h2>
      <div class="row">
        <div class="col-md-6">
          <h3>Test Run #{{ storedTestRuns[0].id }}</h3>
          <RetreiveTestRunComponent :testRunId="storedTestRuns[0].id" :teamId="storedTestRuns[0].team"/>
        </div>
        <div class="col-md-6" >
          <h3>Test Run #{{ storedTestRuns[1].id }}</h3>
            <RetreiveTestRunComponent :testRunId="storedTestRuns[1].id" :teamId="storedTestRuns[1].team"/>
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
    }
},

};
</script>
  

  