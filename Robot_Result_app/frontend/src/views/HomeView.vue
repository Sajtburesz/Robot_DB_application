<template>
  <div class="dashboard-container">
    <div class="row">
      <!-- Each of these columns will take up 6 parts of the available 12 parts of the row on small screens and larger -->
      <div class="col-sm-6 mb-4">
        <div class="chart-card">
          <TestCaseFailureChart/>
        </div>
      </div>
      
      <div class="col-sm-6 mb-4">
        <div class="chart-card">
         <TestCaseDurationChart/>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- TreeMap Chart -->
      <!-- This column will take up the full width of the row on all screen sizes -->
      <div class="col-12 mb-4">
        <div class="chart-card">
          <TreeMapChart />
        </div>
      </div>
    </div>

    <div class="row">
      <!-- TimeLine Chart -->
      <!-- This column will take up the full width of the row on all screen sizes -->
      <div class="col-12 mb-4">
        <div class="chart-card">
          <TimeLineChart />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TestCaseFailureChart from "@/components/TopFailingTC.vue";
import TreeMapChart from "@/components/TreeMap.vue";
import TimeLineChart from "@/components/TimeLine.vue";
import TestCaseDurationChart from "@/components/TestCaseDuration.vue";


export default {
  components: {
    TestCaseFailureChart,
    TreeMapChart,
    TimeLineChart,
    TestCaseDurationChart
  },
};

</script>

<style>
.dashboard-container {
  padding: 2rem;
  max-width: 100%;
  margin: auto;
}

.chart-card {
  background: #ffffff;
  border-radius: 0.5rem;
  box-shadow: 0 0.46875rem 2.1875rem rgb(90 97 105 / 10%), 
              0 0.9375rem 1.40625rem rgb(90 97 105 / 10%), 
              0 0.25rem 0.53125rem rgb(90 97 105 / 12%), 
              0 0.125rem 0.1875rem rgb(90 97 105 / 10%);
  padding: 1.5rem;
  margin-bottom: 2rem;
  max-height: 80vh;
  height: auto;
}


@media (min-width: 992px) {
  .col-lg-6 {
    flex: 0 0 50%;
    max-width: 50%;
  }
}

@media (min-width: 768px) {
  .col-md-12 {
    flex: 0 0 100%;
    max-width: 100%;
  }
}

/* Add any additional custom styles for your dashboard here */
</style>