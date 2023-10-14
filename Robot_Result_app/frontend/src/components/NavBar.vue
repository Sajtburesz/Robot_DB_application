<template>
  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg navbar-light bg-alice-blue">
    <!-- Container wrapper -->
    <div class="container-fluid">
      <!-- Toggle button -->
      <button class="navbar-toggler" type="button" data-mdb-toggle="collapse" data-mdb-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <i class="fas fa-bars"></i>
      </button>

      <!-- Collapsible wrapper -->
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <!-- Navbar brand -->
        <router-link class="navbar-brand mt-lg-o" :to="{ name: 'home' }">
          <img src="https://upload.wikimedia.org/wikipedia/commons/e/e4/Robot-framework-logo.png" height="40"
            alt="MDB Logo" loading="lazy" />
        </router-link>
        <!-- Left links -->
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link fw-bold" href="#">Dashboard</a>
          </li>
          <li class="nav-item">
            <router-link class="nav-link fw-bold" :to="{name : 'CreateTeamView'}">Team</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link fw-bold" href="#">Projects</a>
          </li>
        </ul>
        <!-- Left links -->
      </div>
      <!-- Collapsible wrapper -->

      <!-- Right elements -->
      <div class="d-flex align-items-center">
        <!-- Avatar -->
        <a class="nav-link dropdown-toggle d-flex align-items-center" href="#" id="navbarDropdownMenuLink" type="button"
          data-bs-toggle="dropdown" aria-expanded="false">
          <img src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img (31).webp" class="rounded-circle" height="50"
            alt="Portrait of a Woman" loading="lazy" />
        </a>
        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdownMenuLink">
          <li>
            <router-link class="dropdown-item" :to="{name : 'RetreiveUpdateDestroyeProfileView'}">My profile</router-link>
          </li>
          <li>
            <a class="dropdown-item" href="#">Settings</a>
          </li>
          <li>
            <a class="dropdown-item" href="/accounts/logout/">Logout</a>
          </li>
        </ul>
      </div>
    </div>
    <!-- Container wrapper -->
  </nav>
  <!-- Navbar -->
</template>

<script>
export default {
  name: "NavBarComponent",
};
</script>
