<template>
  <div class="home">
    <div class="container-fluid">
      <div class="row">
        <div class="col">
    <TestCaseFailureChart></TestCaseFailureChart>
        </div>
        <div class="col">
    <TestCaseFailureChart></TestCaseFailureChart>

        </div>
        <div class="col">
    <TestCaseFailureChart></TestCaseFailureChart>

        </div>

  </div>
  </div>
  </div>
</template>
<script>
import TestCaseFailureChart from "@/components/TopFailingTC.vue";

export default {
    components: {
      TestCaseFailureChart,
    },
};

</script>
