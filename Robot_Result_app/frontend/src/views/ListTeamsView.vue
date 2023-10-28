<template>
    <div class="vh-100 my-5">
        <div class="container">
            <!-- Two-column layout: LeftSideMenu and TeamList -->
            <div class="row">

                <!-- Left Side Menu -->
                <div class="col-md-2 border-end border-2">
                    <LeftSideTeamMenu></LeftSideTeamMenu>
                </div>

                <!-- Team List -->
                <div class="col-md-10 d-flex align-items-center">
                    <div class="w-100">
                        <!-- Team Card Loop -->
                        <div class="card mb-3 bg-light-sky-blue shadow rounded" v-for="team in teams" :key="team.id">
                            <router-link :to="{ name: 'RetreiveUpdateDestroyTeamView', params: { teamId: team.id } }">
                                <div class="card-body ">
                                    <h5 class="card-title">Team: {{ team.name }}</h5>
                                    <p class="card-text">Owner: {{ team.owner_name }}</p>
                                </div>
                            </router-link>
                        </div>
                        <nav aria-label="..." v-if="teams.length != 0">
                            <ul class="pagination">
                                <li class="page-item" :class="{disabled : !this.prevUrl}">
                                    <span class="page-link btn" @click="getPaginatedList(this.prevUrl)">Previous</span>
                                </li>
                                <li class="page-item" :class="{disabled : !this.nextUrl}">
                                    <a class="page-link btn" @click="getPaginatedList(this.nextUrl)">Next</a>
                                </li>
                            </ul>
                        </nav>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import LeftSideTeamMenu from "@/components/LeftSideTeamMenu.vue";
import { axios } from "@/common/api.service.js";

export default {
    name: "ListTeamView",
    components: {
        LeftSideTeamMenu
    },
    data() {
        return {
            teams: [],
            nextUrl: '',
            prevUrl: '',
        };
    },
    async created() {
        let username = this.getCookie('username');

        const response = await axios.get("/api/v1/users/" + username + "/teams/");

        this.nextUrl = response.data.next;
        this.prevUrl = response.data.previous;

        this.teams = response.data.results;

    },
    methods: {
        async getPaginatedList(url) {

            const response = await axios.get(url);

            this.nextUrl = response.data.next;
            this.prevUrl = response.data.previous;

            this.teams = response.data.results;
        },
        getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        },
    }
}
</script>
