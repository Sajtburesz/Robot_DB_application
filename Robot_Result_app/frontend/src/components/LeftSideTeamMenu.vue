<template>
    <div class="nav nav-pills flex-column mb-auto bg-seasalt">
        <li class="nav-item m-1 p-1 border-bottom">
            <router-link class="nav-link" :to="{name : 'CreateTeamView'}" active-class="active-link">
                <span class="fw-bold" active-class="active-text">Create Team</span>
            </router-link>
        </li>
        <li class="nav-item m-1 p-1">
            <router-link class="nav-link" :to="{name : 'ListTeamsView'}" active-class="active-link">
                <span class="fw-bold" active-class="active-text">List Teams</span>
            </router-link>
        </li>
    </div>
</template>

<script>
export default {
    name: "LeftSideTeamMenu",
}
</script>

<style scoped>
.nav-link {
  color: black !important;
  width: 100%;
  transition: background-color 0.3s ease;
}

.nav-link:hover {
  background-color: #d0d0d0;  
}

.active-link {
  background-color: #B4BBC2; 
}

.active-text{
    color: #f7f7f7ff;
}
</style>
