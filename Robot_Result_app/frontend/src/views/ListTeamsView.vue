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
              <div class="row">
                <div class="col-12" v-for="team in teams" :key="team.id">
                    <router-link :to="{ name: 'RetreiveUpdateDestroyTeamView', params: { teamId: team.id } }" class="no-underline">
                        <div class="team-card horizontal">
                            <div class="team-id">#{{ team.id }}</div>
                            <div class="content">
                            <h2 class="team-name">{{ team.name }}</h2>
                            <p class="team-owner">Owner: <span>{{ team.owner_name }}</span></p>
                            </div>
                        </div>
                    </router-link>
                </div>
              </div>
              <!-- Pagination -->
              <nav aria-label="Page navigation" v-if="teams.length > 0">
                <ul class="pagination justify-content-center">
                  <li class="page-item" :class="{ disabled: !prevUrl }">
                    <span class="page-link" @click="getPaginatedList(prevUrl)">Previous</span>
                  </li>
                  <li class="page-item" :class="{ disabled: !nextUrl }">
                    <a class="page-link" @click="getPaginatedList(nextUrl)">Next</a>
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
        const username = await axios.get("/auth/users/me/");

        const response = await axios.get("/api/v1/users/" + username.data.username + "/teams/");

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

    }
}
</script>

<style scoped>
.team-card.horizontal {
    background: #E9F1FA;
    display: flex;
    align-items: center;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    border-left: 4px solid #3a6f8f;
  }
  
  .team-id {
    color: #3a6f8f;
    font-size: 1.2rem;
    font-weight: 500;
    margin-right: 1rem;
  }
  
  .content {
    flex-grow: 1;
  }
  
  .team-name {
    color: #333;
    margin-bottom: 0.25rem;
  }
  
  .team-owner {
    color: #777;
    font-size: 0.8rem;
    span {
      font-weight: normal;
    }
  }
  
  .pagination .page-link {
    color: #3a6f8f;
    transition: background-color 0.3s ease;
  }
  
  .pagination .page-link:hover {
    background-color: #a3d5ff;
    color: #ffffff;
  }

  .no-underline {
  text-decoration: none;
    }

    .page-item:not(.disabled) .page-link {
  cursor: pointer;
}
  </style>