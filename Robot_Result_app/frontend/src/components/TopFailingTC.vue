<template>
    <div class="container py-3 ">
        <div class="row mb-3">
            <div class="col-md-6">
                <label for="team-select" class="form-label text-ucla-blue">Team:</label>
                <select id="team-select" class="form-select bg-seasalt text-jet" v-model="selectedTeam" @change="fetchFailingTestcases">
                    <option v-for="team in teams" :key="team.id" :value="team.id">{{ team.name }}</option>
                </select>
            </div>
        </div>

        <div class="row">
            <div class="col">
                <apexchart v-if="loaded" type="bar" :options="chartOptions" :series="series"></apexchart>
            </div>
        </div>
    </div>
</template>

<script>
import { axios } from "@/common/api.service.js";
import VueApexCharts from 'vue3-apexcharts';

export default {
    name: "TestCaseFailureChart",
    components: {
        apexchart: VueApexCharts,
    },
    data() {
        return {
            loaded: false,
            chartOptions: {
                chart: {
                    id: 'top-failing-test-cases',
                    type: 'bar',
                },
                xaxis: {
                    categories: []
                },
                plotOptions: {
                    bar: {
                        horizontal: false,
                    }
                },
                dataLabels: {
                    enabled: false
                },
                title: {
                    text: 'Top Failing Test Cases'
                },
            },
            series: [
                {
                    name: 'Failures',
                    data: []
                }
            ],
            teams: [],
            selectedTeam: null
        };
    },
    async mounted() {
        await this.fetchTeams();
        await this.fetchFailingTestcases();
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
                this.selectedTeam = this.teams[0]?.id;
            } catch (error) {
                console.error("Error fetching user teams:", error);
            }
        },
        async fetchFailingTestcases() {
            if (this.selectedTeam) {
                try {
                    const response = await axios.get(`/api/v1/top-failing-testcases/${this.selectedTeam}/`);
                    this.series[0].data = response.data.map(item => item.failure_count);
                    this.chartOptions.xaxis.categories = response.data.map(item => item.name);
                    this.loaded = true;
                } catch (error) {
                    console.error("Error fetching failing test cases:", error);
                }
            }
        }
    }
};
</script>
  