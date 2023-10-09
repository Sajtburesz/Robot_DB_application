<template>
    <div class="d-flex justify-content-center vh-100">
        <!-- Two-column layout: LeftSideMenu and TeamList -->
        <div class="row bg-seasalt w-75">

            <!-- Left Side Menu -->
            <div class="col-md-2 border-end">
                <LeftSideTeamMenu></LeftSideTeamMenu>
            </div>

            <!-- Team List -->
            <div class="col-md-10 d-flex align-items-center">
                <div class="w-100">
                    <!-- Team Card Loop -->
                    <div class="card mb-3 bg-light-sky-blue" v-for="team in teams" :key="team.id">
                        <router-link :to="{name : 'RetreiveUpdateDestroyTeamView',params: { teamId: team.id }}">
                            <div class="card-body">
                                <h5 class="card-title">{{ team.id }}. {{ team.name }}</h5>
                                <p class="card-text">Owner: {{ team.owner_name}}</p>
                            </div>
                        </router-link>
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
            teams: []
        };
    },
    async created() {
        let username = this.getCookie('username');
        let allTeams = [];

        let nextUrl = "/api/v1/users/" + username + "/teams/";

        while (nextUrl) {
            const response = await axios.get(nextUrl);
            allTeams = allTeams.concat(response.data.results);
            nextUrl = response.data.next;
            console.log(response.data);
        }

        this.teams = allTeams;
        console.log(this.teams);
    },
    methods: {
        getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        },
    }
}
</script>
