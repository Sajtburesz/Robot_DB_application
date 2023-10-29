<template>
  <RetreiveTestRunComponent :testRunId="this.testRunId" :teamId="this.teamId"></RetreiveTestRunComponent>
</template>


<script>
import RetreiveTestRunComponent from "@/components/RetreiveTestRun.vue";

export default {
    components: {
        RetreiveTestRunComponent,
    },
    data() {
        return {
            teamId: this.$route.params.teamId,
            testRunId: this.$route.params.testRunId
        };
    },

};
</script>