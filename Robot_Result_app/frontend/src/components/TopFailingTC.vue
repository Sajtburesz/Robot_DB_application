<template>
    <div class="container py-3 ">
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
        </div>

        <div class="row">
            <div class="col">
                <apexchart v-if="loaded && this.series[0].data.length" type="bar" :options="chartOptions" :series="series"></apexchart>
                <div v-else class="no-data-message">
                    No data available with these parameters.
                </div>
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
                    height: 'auto',
                },
                xaxis: {
                    categories: [], // This will be set dynamically
                labels: {
                    trim: true,
                    rotate: -45,
                    rotateAlways: true,
                    minHeight: 100,
                },
                tooltip: {
                    enabled: true // Disable tooltip if labels are too long
                }
                },
                yaxis: {
                labels: {
                    formatter: (val) => {
                        return Math.round(val); // Rounds to the nearest whole number
                    }
                },
                tickAmount: 5 // Adjust to control the number of ticks
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
                colors: ['#3a6f8fff']
            },
            series: [
                {
                    name: 'Failures',
                    data: []
                }
            ],
            teams: [],
            selectedTeam: null,
            selectedTeamName: null,
            teamFilter: '',
            filteredTeams: [],
        };
    },
    async mounted() {
        await this.fetchTeams();
        await this.fetchFailingTestcases();
    },
    watch: {
        selectedTeam(newTeam, oldTeam) {
            if (newTeam !== oldTeam) {
                this.fetchFailingTestcases();
            }
        }
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

                this.teams.unshift({id: 'public', name: 'public'});

                this.filteredTeams = this.teams;
                this.selectedTeam = this.teams[0]?.id;
                this.selectedTeamName = this.teams[0]?.name;
            } catch (error) {
                this.$toast.error(`Error fetching user teams.`);
            }
        },
        async fetchFailingTestcases() {
            if (this.selectedTeam) {
                try {
                    const response = await axios.get(`/api/v1/top-failing-testcases/${this.selectedTeam}/`);
                    this.series[0].data = response.data.map(item => item.failure_count);
                    this.chartOptions = {
                        ...this.chartOptions,
                        xaxis: {
                            ...this.chartOptions.xaxis,
                            categories: response.data.map(item => item.name)
                        }
                    };
                    this.loaded = true;
                } catch (error) {
                    this.$toast.error(`Error fetching failing test cases.`);
                }
            }
        },
    
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
        },
        toggleTeamDropdown() {
            this.$refs.teamDropdown.classList.toggle('show');
        },
    }
};
</script>
  