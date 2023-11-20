<template>
    <div class="container py-3">
        <div class="row mb-3">
            <div class="col-md-6">
                <label for="team-dropdown" class="form-label text-ucla-blue">Team:</label>
                <div class="dropdown" ref="teamDropdown">
                    <button class="btn btn-secondary dropdown-toggle w-100 bg-ucla-blue text-seasalt truncate" type="button"
                            id="team-dropdown" data-bs-toggle="dropdown" aria-expanded="false" @click="toggleTeamDropdown()">
                        {{ selectedTeamName || 'Select a team' }}
                    </button>
                    <div class="dropdown-menu w-100" aria-labelledby="team-dropdown">
                        <div class="p-2">
                            <input type="text" class="form-control mb-2 bg-seasalt text-jet" v-model="teamFilter"
                                placeholder="Type to filter..." @input="filterTeams()">
                        </div>
                        <ul class="list-group overflow-auto" style="max-height: 200px;">
                            <li class="list-group-item bg-seasalt text-jet bg-animation clickable-item " href="#"
                                v-for="team in filteredTeams" :key="team.id" @click.prevent="selectTeam(team)">
                                {{ team.name }}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <label for="start-date" class="form-label text-ucla-blue">Start Date:</label>
                <input id="start-date" type="date" class="form-control bg-seasalt text-jet" v-model="startDate" :min="this.minDate" :max="this.maxDate" @change="fetchTreemapData">
            </div>
        </div>

        <div class="row">
            <div class="col">
                <apexchart v-if="loaded" type="treemap" :options="chartOptions" :series="series"></apexchart>
            </div>
        </div>
    </div>
</template>

<script>
import { axios } from "@/common/api.service.js";
import VueApexCharts from 'vue3-apexcharts';

export default {
    name: "TreeMapChart",
    components: {
        apexchart: VueApexCharts,
    },
    data() {
        return {
            loaded: false,
            chartOptions: {
                legend: {
                    show: false // Hide the legend
                },
                chart: {
                    height: 350,
                    type: 'treemap',
                },
                tooltip: {
                    enabled: true,
                },

            },
            series: [],
            teams: [],
            selectedTeam: null,
            selectedTeamName: null,
            teamFilter: '',
            filteredTeams: [],

            startDate: '', // Initially empty, will be set to the oldest date
            minDate: '', // Minimum date for the date input
            maxDate: '', // Maximum date for the date input
        };
    },
    async mounted() {
        await this.fetchTeams();
        await this.fetchDateRange();
    },
    methods: {
        async fetchTeams() {
            try {
                const user = await axios.get('/auth/users/me/');
                let url = '/api/v1/users/' + user.data.username + '/teams/';
                let allTeams = [];
                while (url) {
                    const response = await axios.get(url);
                    allTeams = allTeams.concat(response.data.results.map(team => ({ id: team.id, name: team.name })));
                    url = response.data.next;
                }
                this.teams = allTeams;
                this.filteredTeams = allTeams;
                this.selectedTeam = this.teams[0]?.id;
                this.selectedTeamName = this.teams[0]?.name;
            } catch (error) {
                console.error("Error fetching user teams:", error);
            }
        },
        async fetchDateRange() {
            try {
                const response = await axios.get(`/api/v1/date-range/${this.selectedTeam}/`);
                this.minDate = response.data.min_date.split('T')[0];
                this.maxDate = response.data.max_date.split('T')[0];
                this.startDate = this.minDate; // Set the start date to the oldest date
                console.log(this.minDate)
                this.fetchTreemapData(); // Fetch heatmap data for the initial date
            } catch (error) {
                console.error("Error fetching heatmap date range:", error);
            }
        },
        async fetchTreemapData() {
            if (this.selectedTeam && this.startDate) {
                try {
                    const response = await axios.get(`/api/v1/treemap-data/${this.selectedTeam}/`, {
                        params: {
                            start_date: this.startDate
                        }
                    });
                    // Transform the response data to match the expected format for treemap
                    this.series = [{
                        data: response.data.map(item => ({
                            x: item.suite_name,
                            y: item.total_cases, // Use total_cases for the size of the rectangle
                            fillColor: this.getFillColor(item.failed_cases) // Use failed_cases to determine color
                        }))
                    }];

                    this.loaded = true;
                } catch (error) {
                    console.error("Error fetching heatmap data:", error);
                }
            }
        },
        getFillColor(failedCases) {
            if (failedCases < 1) {
                return '#00A100'; // Green for low failure count
            } else if (failedCases < 3) {
                return '#FFB200'; // Orange for medium failure count
            } else {
                return '#FF0000'; // Red for high failure count
            }
        },

         // dropdown for teams
         filterTeams() {
        if (this.teamFilter) {
            this.filteredTeams = this.teams.filter((team) =>
                team.name.toLowerCase().includes(this.teamFilter.toLowerCase())
            );
        } else {
            this.filteredTeams = this.teams;
        }
        },
        selectTeam(team) {
            this.selectedTeam = team.id;
            this.selectedTeamName = team.name;
            this.teamFilter = '';
            this.filteredTeams = this.teams;
            this.$refs.teamDropdown.classList.remove('show');
            this.selectedTeamName = team.name;
            this.fetchDateRange();
            // Call any additional methods needed after team selection
        },
        toggleTeamDropdown() {
            this.$refs.teamDropdown.classList.toggle('show');
        },
    }
};
</script>
