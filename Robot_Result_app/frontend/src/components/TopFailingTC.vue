<template>
    <div>
        <select v-model="selectedTeam" @change="fetchFailingTestcases">
            <option v-for="team in teams" :key="team.id" :value="team.id">{{ team.name }}</option>
        </select>

        <div v-if="loading">
            Loading...
        </div>

        <canvas ref="chart"></canvas>
    </div>
</template>
  
<script>
import { ref, onMounted, nextTick } from 'vue';
import { Chart, BarController, LinearScale, CategoryScale, BarElement } from 'chart.js';
import { axios } from "@/common/api.service.js";

Chart.register(BarController, LinearScale, CategoryScale, BarElement);
export default {
    name: 'TestCaseFailureChart',
    setup() {
        const chart = ref(null);
        const selectedTeam = ref(null);
        const teams = ref([]);
        const loading = ref(true);

        const fetchUserTeams = async () => {
            try {
                const user = await axios.get('/auth/users/me/');
                let url = '/api/v1/users/' + user.data.username + '/teams/';
                let allTeams = [];
                while (url) {
                    const response = await axios.get(url);
                    allTeams = allTeams.concat(response.data.results.map(team => ({ id: team.id, name: team.name })));
                    url = response.data.next;
                }
                teams.value = allTeams;
                selectedTeam.value = teams.value[0]?.id;
                fetchFailingTestcases();
            } catch (error) {
                console.error("Error fetching user teams:", error);
            }
        };

        const fetchFailingTestcases = async () => {
            loading.value = true;
            try {
                const response = await axios.get(`/api/v1/top-failing-testcases/${selectedTeam.value}/`);
                await nextTick();  // Ensure DOM updates
                renderChart(response.data);
            } catch (error) {
                console.error("Error fetching failing test cases:", error);
            } finally {
                loading.value = false;
            }
        };

        const renderChart = (data) => {
            const names = data.map(item => item.name);
            const failure_counts = data.map(item => item.failure_count);

            const ctx = chart.value ? chart.value.getContext('2d') : null;

            if (chart.value && typeof chart.value.destroy === 'function') {
                chart.value.destroy();
                chart.value = null;
            }

            chart.value = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: names,
                    datasets: [{
                        label: 'Failure Count',
                        data: failure_counts,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        };

        onMounted(fetchUserTeams);

        return { chart, teams, selectedTeam, loading, fetchFailingTestcases };
    }
};
</script>
  