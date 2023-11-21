<template>
    <div class="container py-3">
        <div class="row mb-3">
            <div class="col-md-3">
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
            <div class="col-md-3">
                <label for="date" class="form-label text-ucla-blue">Date:</label>
                <input id="date" type="month" placeholder="YYYY.MM" class="form-control bg-seasalt text-jet" v-model="date"
                    @change="selectedSuite ? fetchData() : null">
            </div>
            <div class="col-md-6" v-if="selectedTeam">
                <label for="suite-dropdown" class="form-label text-ucla-blue">Suite:</label>
                <div class="dropdown" ref="dropdown">
                    <button class="btn btn-secondary dropdown-toggle w-100 bg-ucla-blue text-seasalt truncate" type="button"
                        id="suite-dropdown" data-bs-toggle="dropdown" aria-expanded="false" @click="toggleDropdown">
                        {{ selectedSuite || 'Select a suite' }}
                    </button>
                    <div class="dropdown-menu w-100" aria-labelledby="suite-dropdown">
                        <div class="p-2">
                            <input type="text" class="form-control mb-2 bg-seasalt text-jet" v-model="suiteFilter"
                                placeholder="Type to filter..." @input="filterSuites">
                        </div>
                        <ul class="list-group overflow-auto" style="max-height: 200px;">
                            <li class="list-group-item bg-seasalt text-jet bg-animation clickable-item" href="#"
                                v-for="suite in filteredSuites" :key="suite" @click.prevent="selectSuite(suite)">
                                {{ suite }}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col">
                <apexchart v-if="this.chartSeries.length" type="heatmap" :options="chartOptions" :series="chartSeries"></apexchart>
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
    components: {
        apexchart: VueApexCharts,
    },
    data() {
        return {
            selectedTeam: null,
            selectedTeamName: null,
            teamFilter: '',
            filteredTeams: [],

            date: '',

            minDate: '', 
            maxDate: '',

            teams: [],
            selectedSuite: null,
            suiteFilter: '',
            filteredSuites: [],

            chartOptions: {
                chart: {
                    type: 'heatmap',
                    height: 'auto',
                    toolbar: {
                        show: true
                    }
                },
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    show: true,
                    width: 0.2, // Width of the stroke line
                    colors: ['#333333ff'],
                },

                fill: {
                    type: 'solid',
                    opacity: 1
                },
                colors: ["#3a6f8fff"],
                title: {
                    text: 'Testcase Duration Heatmap'
                },
                xaxis: {
                    type: 'category',
                    categories: [], // This will be dynamically set
                    labels: {
                        formatter: (val) => {

                            const date = new Date(val);
                            return `${date.getUTCFullYear()}.${date.getMonth() + 1}.${date.getDate()}`;
                        }
                    }
                },
                yaxis: {
                    labels: {
                        maxWidth: 160,
                        formatter: (val) => {
                            // Truncate long labels on the y-axis
                            return val.length > 15 ? val.substring(0, 15) + '...' : val;
                        }
                    }
                },
                tooltip: {
                    y: {
                        formatter: function (value) {
                            return value + ' seconds';
                        }
                    }
                },
                plotOptions: {
                    heatmap: {
                        shadeIntensity: 0.5,
                        radius: 0,
                        useFillColorAsStroke: false,
                        colorScale: {
                            ranges: [
                                {
                                    from: -Infinity,
                                    to: 5,
                                    color: '#00A100',
                                    name: 'up to 5% above average',
                                },
                                {
                                    from: 5.01,
                                    to: 10,
                                    color: '#FFB200',
                                    name: '5% to 10% above average',
                                },
                                {
                                    from: 10.01,
                                    to: Infinity,
                                    color: '#FF0000',
                                    name: 'more than 10% above average',
                                },
                            ],
                        },
                    },
                },
            },
            chartSeries: [],
        };
    },

    async mounted() {
        await this.fetchTeams();
        await this.fetchDateRange();
    },

    methods: {
        fetchData() {
            const apiUrl = `/api/v1/duration-heatmap/${this.selectedTeam}/`;
            const payload = {
                suite_name: this.selectedSuite,
                date: this.date,
            };

            axios
                .post(apiUrl, payload)
                .then((response) => {
                    this.processData(response.data);
                })
                .catch((error) => {
                    this.$toast.error(`Error fetching data: ${error.request.statusText}`);
                });
        },
        async fetchDateRange() {
            try {
                const response = await axios.get(`/api/v1/date-range/${this.selectedTeam}/`);
                this.minDate = response.data.min_date.split('T')[0].slice(0, 7);
                this.maxDate = response.data.max_date.split('T')[0].slice(0, 7);
                this.date = this.maxDate;
                await this.fetchSuites(); 
            } catch (error) {
                this.chartSeries = [];
                this.$toast.error(`Error fetching heatmap date range.`);
            }
        },
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
        async fetchSuites() {
            try {
                this.selectedSuite = null;
                this.suites = [];
                const response = await axios.get(`/api/v1/suite-names/${this.selectedTeam}/`);
                this.suites = response.data;
                this.filteredSuites = this.suites;
                this.selectSuite(this.filteredSuites[0]);
            } catch (error) {
                this.$toast.error(`Error fetching suite names.`);
            }
        },
        filterSuites() {
            if (this.suiteFilter) {
                this.filteredSuites = this.suites.filter((suite) =>
                    suite.toLowerCase().includes(this.suiteFilter.toLowerCase())
                );
            } else {
                this.filteredSuites = this.suites;
            }
        },
        selectSuite(suite) {
            this.selectedSuite = suite;
            this.suiteFilter = '';
            this.filteredSuites = this.suites;
            this.$refs.dropdown.classList.remove('show');
            this.fetchData();
        },
        toggleDropdown() {
            this.$refs.dropdown.classList.toggle('show');
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
        processData(data) {
            // Process and map the data to fit the chartSeries format
            this.chartSeries = data.map((testcase) => {
                const overallAverageDuration = testcase.overall_average_duration;
                return {
                    name: testcase.testcase_name,
                    data: testcase.daily_averages.map((dailyData) => {
                        // Calculate deviation percentage from the overall average duration
                        const deviationPercentage = ((dailyData.average_duration - overallAverageDuration) / overallAverageDuration) * 100;
                        return {
                            x: dailyData.day,
                            y: deviationPercentage.toFixed(2), // Display the deviation percentage up to 2 decimal places
                            averageDuration: dailyData.average_duration // Store the average duration for tooltip
                        };
                    }),
                };
            });

            // Update the categories for the x-axis based on the data
            if (this.chartSeries.length > 0) {
                this.chartOptions = {
                    ...this.chartOptions,
                    xaxis: {
                        ...this.chartOptions.xaxis,
                        categories: this.chartSeries[0].data.map(d => d.x)
                    },
                    tooltip: {
                        ...this.chartOptions.tooltip,
                        y: {
                            formatter: function (value, { seriesIndex, dataPointIndex, w }) {
                                // Retrieve the average duration from the stored data and display it
                                return w.config.series[seriesIndex].data[dataPointIndex].averageDuration.toFixed(2) + ' seconds';
                            }
                        }
                    },
                };
            }
        },
    },
};
</script>
<style>
.clickable-item {
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.clickable-item:hover {
    background-color: #a3d5ff;
    /* light-sky-blue */
}

.chart-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    color: #aaa;
}

.truncate {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>