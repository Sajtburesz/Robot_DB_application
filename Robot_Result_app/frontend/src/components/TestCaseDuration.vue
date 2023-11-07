<template>
    <div class="container py-3">
        <div class="row mb-3">
            <div class="col-md-3">
                <label for="team-select" class="form-label text-ucla-blue">Team:</label>
                <select id="team-select" class="form-select bg-seasalt text-jet" v-model="selectedTeam" @change="fetchSuites()">
                    <option v-for="team in teams" :key="team.id" :value="team.id">
                        {{ team.name }}
                    </option>
                </select>
            </div>
            <div class="col-md-3">
                <label for="date" class="form-label text-ucla-blue">Date:</label>
                <input id="date" type="month" class="form-control bg-seasalt text-jet" v-model="date" @change="selectedSuite ? fetchData() : null">
            </div>
            <div class="col-md-6" v-if="selectedTeam">
                <label for="suite-dropdown" class="form-label text-ucla-blue">Suite:</label>
                <div class="dropdown" ref="dropdown">
                    <button class="btn btn-secondary dropdown-toggle w-100 bg-ucla-blue text-seasalt" type="button" id="suite-dropdown"
                            data-bs-toggle="dropdown" aria-expanded="false" @click="toggleDropdown">
                        {{ selectedSuite || 'Select a suite' }}
                    </button>
                    <div class="dropdown-menu w-100" aria-labelledby="suite-dropdown">
                        <div class="p-2">
                            <input type="text" class="form-control mb-2 bg-seasalt text-jet" v-model="suiteFilter" placeholder="Type to filter..."
                                   @input="filterSuites">
                        </div>
                        <ul class="list-group overflow-auto" style="max-height: 200px;">
                            <li class="list-group-item bg-seasalt text-jet bg-animation clickable-item" href="#" v-for="suite in filteredSuites" :key="suite"
                                @click.prevent="selectSuite(suite)">
                                {{ suite }}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col">
                <apexchart v-if="chartSeries.length" type="heatmap" :options="chartOptions" :series="chartSeries"></apexchart>
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
            date: '',
            teams: [],
            selectedSuite: null,
            suiteFilter: '',
            filteredSuites: [],

            chartOptions: {
                chart: {
                    type: 'heatmap',
                    height: 350,
                    toolbar: {
                        show: true
                    }
                },
                dataLabels: {
                    enabled: false
                },
                colors: ["#008FFB"],
                title: {
                    text: 'Testcase Duration Heatmap'
                },
                xaxis: {
                    type: 'category',
                    categories: []
                },
                yaxis: {
                    title: {
                        text: 'Testcase'
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
                        useFillColorAsStroke: true,
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
            chartSeries: []
        };
    },

    async mounted() {
        await this.fetchTeams();
        await this.fetchSuites(); // Fetch the date range for the date input
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
                    console.error('Error fetching data:', error);
                });
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
                this.selectedTeam = this.teams[0]?.id;
            } catch (error) {
                console.error("Error fetching user teams:", error);
            }
        },
        async fetchSuites() {
            try {
                this.selectedSuite = null;
                this.suites = [];
                const response = await axios.get(`/api/v1/suite-names/${this.selectedTeam}/`);
                this.suites = response.data;
                this.filteredSuites = this.suites;
            } catch (error) {
                console.error("Error fetching suite names:", error);
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
        background-color: #a3d5ff; /* light-sky-blue */
    }
</style>