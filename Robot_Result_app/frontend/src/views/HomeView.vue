<template>
  <div class="dashboard-container">
    <!-- Use row-eq-height to ensure that cards in the same row have equal height -->
    <div class="row row-eq-height">
      <div class="col-sm-12 col-md-6 mb-4">
        <div class="chart-card">
          <TestCaseFailureChart/>
        </div>
      </div>
      
      <div class="col-sm-12 col-md-6 mb-4">
        <div class="chart-card">
         <TestCaseDurationChart/>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-12 mb-4">
        <div class="chart-card">
          <TreeMapChart />
        </div>
      </div>
    </div>

    <div class="row">
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
  /* Flexbox properties to maintain consistent scaling */
  display: flex;
  flex-direction: column;
  /* Minimum height to maintain consistent size */
  min-height: 400px; 
  /* Flex properties to allow card to grow and shrink with equal weight */
  flex-grow: 1;
  flex-shrink: 1;
}

/* Responsive grid adjustments */
@media (min-width: 768px) {
  .col-md-6 {
    /* Ensuring that on medium devices and up, the two chart cards take half the width */
    flex: 0 0 50%;
    max-width: 50%;
  }
  .col-md-12 {
    /* Ensuring that on medium devices and up, the single chart card takes full width */
    flex: 0 0 100%;
    max-width: 100%;
  }
}

/* Ensuring that all cards in the same row have the same height */
.row-eq-height {
  display: flex;
  flex-wrap: wrap;
}

/* Custom styles for card titles or other elements can be added here */
</style>