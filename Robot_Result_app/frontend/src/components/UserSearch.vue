<template>
    <div class="form-outline">
        <input class="form-input" v-model="query" @input="fetchUsersDebounced" placeholder="Search users...">
    </div>
</template>
  
<script>
import { axios } from "@/common/api.service.js";

export default {
    name: "UserSearchComponent",
    data() {
        return {
            query: '',
            users: [],
            debounceTimeout: null,
        };
    },
    methods: {
        fetchUsersDebounced() {

            clearTimeout(this.debounceTimeout);
            if(this.query){
                this.$emit('set-loading', true);
                this.debounceTimeout = setTimeout(this.fetchUsers, 500);
            }else {
                this.users = [];
                this.$emit('set-users', this.users);
            }
        },
        async fetchUsers() {
        
            const response = await axios.get(`/api/v1/users/?username=${this.query}`);
            this.users = response.data.results;
            this.$emit('set-users', this.users);

            this.$emit('set-loading', false);
        },
    },
};
</script>
  
  