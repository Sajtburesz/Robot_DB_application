<template>
    <div class="container py-3">
        <div class="row mb-3">
            <div class="col-md-4">
                <label for="team-select" class="form-label text-ucla-blue">Team:</label>
                <select id="team-select" class="form-select bg-seasalt text-jet" v-model="selectedTeam" @change="fetchDateRange">
                    <option v-for="team in teams" :key="team.id" :value="team.id">{{ team.name }}</option>
                </select>
            </div>

            <div class="col-md-4">
                <label for="start-date" class="form-label text-ucla-blue">Start Date:</label>
                <input id="start-date" type="date" class="form-control bg-seasalt text-jet" v-model="startDate" :min="this.minDate" :max="this.maxDate" @change="fetchTimelineData">
            </div>

            <div class="col-md-4">
                <label for="suite-filter" class="form-label text-ucla-blue">Suite Filter:</label>
                <input id="suite-filter" type="text" class="form-control bg-seasalt text-jet" v-model="suiteFilter" placeholder="Filter by suite name" @input="fetchTimelineData">
            </div>
        </div>

        <div class="row">
            <div class="col vh-100 overflow-auto">
                <apexchart v-if="loaded" type="rangeBar" :options="chartOptions" ref="myChart" :series="rawSeries"></apexchart>
            </div>
        </div>
    </div>
</template>

  
<script>
import { axios } from "@/common/api.service.js";
import VueApexCharts from 'vue3-apexcharts';
import { toRaw } from 'vue';

export default {
    name: "TimeLineChart",
    components: {
        apexchart: VueApexCharts,
    },
    data() {
        return {
            loaded: false,
            series: [
                {
                    data: [],
                },
            ],
            chartOptions: {
                chart: {
                    type: 'rangeBar',
                    height: 350,
                    toolbar: {
                        show: true,
                        tools: {
                            download: true,
                            selection: true,
                            zoom: true,
                            zoomin: true,
                            zoomout: true,
                            pan: true,
                            reset: true
                        },
                        autoSelected: 'zoom'
                    },
                },
                plotOptions: {
                    bar: {
                        horizontal: true,
                        barHeight: '100%', // Adjust this value as needed
                    }
                },
                xaxis: {
                    type: 'datetime',
                    tickAmount: 10,
                },  
                stroke: {
                    width: 1
                },
                yaxis: {
                    labels: {
                        show: true,
                        align: 'right',
                        maxWidth: 160,
                    },
                },
                fill: {
                    type: 'solid',
                    opacity: 0.6
                },
                legend: {
                    position: 'top',
                    horizontalAlign: 'left'
                },
                title: {
                    text: 'Test Case Fail Periods',
                    align: 'center',
                },
                
            },
            teams: [],
            selectedTeam: null,
            startDate: '', // Initially empty, will be set to the oldest date
            minDate: '', // Minimum date for the date input
            maxDate: '', // Maximum date for the date input
            suiteFilter: '', // Filter for suite name
        };
    },
    computed: {
        rawSeries() {
            return toRaw(this.series);
        }
    },
    async mounted() {
        await this.fetchTeams();
        await this.fetchDateRange(); // Fetch the date range for the date input
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
        async fetchDateRange() {
            try {
                const response = await axios.get(`/api/v1/date-range/${this.selectedTeam}/`);
                this.minDate = response.data.min_date.split('T')[0];
                this.maxDate = response.data.max_date.split('T')[0];
                this.startDate = this.minDate; // Set the start date to the oldest date
                await this.fetchTimelineData();
            } catch (error) {
                console.error("Error fetching heatmap date range:", error);
            }
        },

        async fetchTimelineData() {
            if (this.selectedTeam && this.startDate) {
                this.loaded = false;
                try {
                    // Replace with the actual endpoint that returns timeline data
                    const response = await axios.get(`/api/v1/timeline-data/${this.selectedTeam}/`, {
                        params: {
                            start_date: this.startDate,
                            suite_filter: this.suiteFilter
                        }
                    });

                    // Transform the response data to match the expected format for timeline
                    const timelineData = response.data.flatMap(instance =>
                        instance.fail_periods.map(period => {
                            // Split and parse the dates
                            let startDate = new Date(period.start.split('T')[0]);
                            let endDate = new Date(period.end.split('T')[0]);

                            // If the dates are the same, add one day to the end date
                            if (startDate.getTime() === endDate.getTime()) {
                                endDate.setDate(endDate.getDate() + 1);
                            }

                            return {
                                x: instance.test_case_name,
                                y: [
                                    startDate.getTime(),
                                    endDate.getTime()
                                ]
                            };
                        })
                    );
                    this.series = [{ data: timelineData }];

                    this.loaded = true;
                } catch (error) {
                    console.error("Error fetching timeline data:", error);
                }
            }
        }
    }
};
</script>


<style>
    .chart-container {
    max-height: 700px; /* Fixed maximum height for the container */
    }
</style>
