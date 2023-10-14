<template>
    <div>
        <input v-model="query" @input="fetchUsersDebounced" placeholder="Search users...">
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

            this.debounceTimeout = setTimeout(this.fetchUsers, 300);
        },
        async fetchUsers() {
            if (this.query) {
                const response = await axios.get(`/api/v1/users/?username=${this.query}`);
                this.users = response.data.results;
                this.$emit('set-users', this.users);
            } else {
                this.users = [];
                this.$emit('set-users', this.users);
            }
        },
    },
};
</script>
  
  