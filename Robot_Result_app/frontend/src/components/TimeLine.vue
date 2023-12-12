<template>
    <div class="container py-3">
        <div class="row mb-3">
            <div class="col-md-4">
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

            <div class="col-md-4">
                <label for="start-date" class="form-label text-ucla-blue">Start Date:</label>
                <input id="start-date" type="date" class="form-control bg-seasalt text-jet" v-model="startDate"
                    :min="this.minDate" :max="this.maxDate" @change="fetchTimelineData">
            </div>

            <div class="col-md-4">
                <label for="suite-filter" class="form-label text-ucla-blue">Suite Filter:</label>
                <input id="suite-filter" type="text" class="form-control bg-seasalt text-jet" v-model="suiteFilter"
                    placeholder="Filter by suite name" @input="fetchTimelineData">
            </div>
        </div>

        <div class="row">
            <div class="col vh-100 overflow-auto">
                <apexchart v-if="loaded && this.series[0].data.length" type="rangeBar" :options="chartOptions" ref="myChart" :series="rawSeries">
                </apexchart>
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
                    height: 'auto',
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
                colors: ['#3a6f8fff'],
                plotOptions: {
                    bar: {
                        horizontal: true,
                        barHeight: '90%', // Adjust this value as needed
                    }
                },
                xaxis: {
                    type: 'datetime',
                    tickamount: 10,
                },
                stroke: {
                    show: true,
                    width: 1, // Width of the stroke line
                    colors: ['#333333ff'], // Color of the stroke, here it's set to white for contrast
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
            selectedTeamName: null,
            teamFilter: '',
            filteredTeams: [],
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
        extractPath(url) {
            if (!url) return null;
            const basePath = '/api/v1/';
            const index = url.indexOf(basePath);
            return index !== -1 ? url.substring(index) : null;
        },
        async fetchTeams() {
            try {
                const user = await axios.get('/auth/users/me/');
                let url = '/api/v1/users/' + user.data.username + '/teams/';
                let allTeams = [];
                while (url) {
                    const response = await axios.get(url);
                    allTeams = allTeams.concat(response.data.results.map(team => ({ id: team.id, name: team.name })));
                    url = this.extractPath(response.data.next);
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
        async fetchDateRange() {
            try {
                const response = await axios.get(`/api/v1/date-range/${this.selectedTeam}/`);
                this.minDate = response.data.min_date.split('T')[0];
                this.maxDate = response.data.max_date.split('T')[0];
                this.startDate = this.minDate; 
                await this.fetchTimelineData();
            } catch (error) {
                this.series = [{data:[]}];
                this.$toast.error(`Error fetching heatmap date range.`);
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
                    this.$toast.error(`Error fetching timeline data.`);
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
            this.fetchDateRange();
            // Call any additional methods needed after team selection
        },
        toggleTeamDropdown() {
            this.$refs.teamDropdown.classList.toggle('show');
        },
    }
};
</script>

