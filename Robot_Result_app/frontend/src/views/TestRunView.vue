<template>
  <div class="d-flex vh-100">
    <div v-if="isPublic" class="bg-light border-end">
      <CommentsComponent :teamId="this.teamId" :testRunId="this.testRunId" />
    </div>
    <div class="flex-grow-1">
        <RetreiveTestRunComponent :testRunId="this.testRunId" :teamId="this.teamId"></RetreiveTestRunComponent>
    </div>
  </div>
</template>


<script>
import RetreiveTestRunComponent from "@/components/RetreiveTestRun.vue";
import CommentsComponent from "@/components/Comments.vue";

export default {
    components: {
        RetreiveTestRunComponent,
        CommentsComponent
    },
    data() {
        return {
            teamId: this.$route.params.teamId,
            testRunId: this.$route.params.testRunId
        };
    },
    computed: {
    isPublic() {
      return this.teamId !== 'public';
    }
  },

};
</script>