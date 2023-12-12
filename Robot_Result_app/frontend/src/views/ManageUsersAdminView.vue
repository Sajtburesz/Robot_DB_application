<template>
    <div class="vh-100 my-5">
        <div class="container">
            <!-- Two-column layout: LeftSideMenu and User List -->
            <div class="row">
                <!-- Left Side Menu -->
                <div class="col-md-2 border-end border-2">
                    <LeftSideAdminMenu />
                </div>

                <!-- User List and Filter -->
                <div class="col-md-10 d-flex align-items-center">
                    <div class="w-100">
                        <!-- Filter -->
                        <div class="mb-4">
                            <input type="text" class="form-control" placeholder="Filter by username..."
                                v-model="filterQuery" @input="handleFilterChange">
                        </div>

                        <!-- User Card Loop -->
                        <div class="row">
                            <div class="col-12" v-for="user in users" :key="user.id">
                                <div class="user-card horizontal">
                                    <div class="content">
                                        <div class="d-flex justify-content-between align-items-center">
                                            <h2 class="user-name">{{ user.username }}</h2>
                                            <div class="d-flex justify-content-end">
                                                <span v-if="user.is_staff || user.is_superuser"
                                                    class="badge bg-secondary align-self-center" style="font-size: smaller;">{{
                                                        badgeText(user) }}</span>
                                                <div>
                                                    <button class="btn btn-link ms-2" @click="toggleCardExpansion(user)">
                                                        <font-awesome-icon
                                                            :icon="user.isExpanded ? 'fa-solid fa-circle-arrow-up' : 'fa-solid fa-circle-arrow-down'"
                                                             />
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                        <!-- Expanded Section -->
                                        <div v-if="user.isExpanded" class="expanded-section border-top border-2 pt-2">
                                            <div class="row">
                                                <!-- Column for Reset Password Form -->
                                                <div class="col-md-6 border-end border-2">
                                                    <div class="mb-3 ">
                                                        <form @submit.prevent="resetPassword(user)">
                                                            <input type="text" name="username" :value="user.username" class="form-control mb-2" autocomplete="username" readonly hidden >
                                                            <input type="password" class="form-control mb-2"
                                                                v-model="user.newPassword" placeholder="New Password"
                                                                autocomplete="new-password">
                                                            <input type="password" class="form-control mb-2"
                                                                v-model="user.confirmPassword"
                                                                placeholder="Confirm New Password"
                                                                autocomplete="new-password">
                                                            <div class=" d-flex justify-content-center align-items-center">
                                                                <button class="btn bg-ucla-blue clickable-item text-seasalt" type="submit">Reset
                                                                    Password</button>
                                                            </div>
                                                        </form>
                                                    </div>
                                                </div>

                                                <!-- Column for Action Buttons -->
                                                <div class="col-md-6 d-flex justify-content-center align-items-center">
                                                    <button v-if="user.is_superuser !== true && isSuperUser" class="btn btn-danger me-2"
                                                    data-bs-toggle="modal" data-bs-target="#userDeleteModal" @click.stop="userForDeletion = user">Delete User</button>
                                                    <button v-if="user.is_staff && isSuperUser && user.is_superuser !== true" class="btn btn-secondary"
                                                    data-bs-toggle="modal" data-bs-target="#manageAdminModal" @click.stop="setAdminModalInfo(user,'Revoke')">Revoke Admin Rights</button>
                                                    <button v-else-if="user.is_staff !== true && user.is_superuser !== true" class="btn btn-secondary"
                                                    data-bs-toggle="modal" data-bs-target="#manageAdminModal" @click.stop="setAdminModalInfo(user,'Grant')">Grant Admin Rights</button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- User Delete Confirmation Modal -->
                        <div v-if="userForDeletion" class="modal fade" tabindex="-1" role="dialog" aria-hidden="true" id="userDeleteModal">
                            <div class="modal-dialog" role="document">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title">Delete User</h5>
                                        <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                    <div class="modal-body">
                                        <p>Are you sure about deleting {{this.userForDeletion.username}} user?</p>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
                                        <button type="button" class="btn btn-danger" @click="deleteUser(this.userForDeletion)"
                                            data-bs-dismiss="modal">Yes</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-if="adminManagementInfo" class="modal fade" tabindex="-1" role="dialog" aria-hidden="true" id="manageAdminModal">
                            <div class="modal-dialog" role="document">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title">Manage Admin Rights</h5>
                                        <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                    <div class="modal-body">
                                        <p>Are you sure about doing action: {{ this.adminManagementInfo.action }} admin rights?</p>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
                                        <button type="button" class="btn btn-danger" @click="manageActionType(this.adminManagementInfo.user,this.adminManagementInfo.action)"
                                            data-bs-dismiss="modal">Yes</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Pagination -->
                        <nav aria-label="Page navigation" v-if="users.length > 0">
                            <ul class="pagination justify-content-center">
                                <li class="page-item" :class="{ disabled: !prevUrl }">
                                    <span class="page-link" @click="fetchUsers(prevUrl)">Previous</span>
                                </li>
                                <li class="page-item" :class="{ disabled: !nextUrl }">
                                    <a class="page-link" @click="fetchUsers(nextUrl)">Next</a>
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
import LeftSideAdminMenu from "@/components/LeftSideAdminMenu.vue";
import { axios } from "@/common/api.service.js";

export default {
    name: "ListUserView",
    components: {
        LeftSideAdminMenu
    },
    data() {
        return {
            users: [],
            nextUrl: '',
            prevUrl: '',
            filterQuery: '',
            debounceTimer: null,
            userForDeletion: {},
            adminManagementInfo: { user: null, action: '' },
        };
    },
    async created() {
        this.fetchUsers("/api/v1/users/");
    },
    computed: {
        isAdmin() {
            this.$store.dispatch('fetchAdminStatus');
            return this.$store.state.isAdmin;
        },
        isSuperUser() {
            this.$store.dispatch('fetchAdminStatus');
            return this.$store.state.isSuperUser;
        }
    },
    methods: {
        async fetchUsers(url) {
            try {
                const response = await axios.get(url + (this.filterQuery ? `?username=${this.filterQuery}` : ''));
                this.nextUrl = response.data.next;
                this.prevUrl = response.data.previous;
                this.users = response.data.results.map(user => ({ ...user, isExpanded: false }));
            } catch (error) {
                this.$toast.error(`Error fetching users.`);
            }
        },
        handleFilterChange() {
            clearTimeout(this.debounceTimer);
            this.debounceTimer = setTimeout(() => {
                this.fetchUsers("/api/v1/users/");
            }, 300);
        },
        toggleCardExpansion(user) {
            user.isExpanded = !user.isExpanded;
        },
        async resetPassword(user) {
            if (user.newPassword === user.confirmPassword) {
                try {
                    await axios.post('/admin/reset-password/', {
                        username: user.username,
                        new_password: user.newPassword
                    });
                    this.$toast.success(`Reseting password for ${user.username} was succesfull.`);
                } catch (error) {
                    this.$toast.error(`Unable to reset password for ${user.username}.`);
                    
                }
            } else {
                this.$toast.error(`Passwords do not match.`);
            }
        },
        async deleteUser(user) {
            try {
                await axios.delete(`/api/v1/users/${user.username}/`);
                this.$toast.success(`Deleting user was successfull.`);
                this.userForDeletion = {};
                this.fetchUsers('/api/v1/users/');
            } catch (error) {
                this.$toast.error(`Unable to delete user.`);
            }
        },
        async grantAdminRights(user) {
            try {
                await axios.post(`/admin/manage-admin/`, {
                    username: user.username
                });
                this.$toast.success(`Successfully granted admin rights to ${user.username}.`);
                this,this.adminManagementInfo = { user: null, action: '' };
                this.fetchUsers('/api/v1/users/');
            } catch (error) {
                this.$toast.error(`Something went wrong during granting admin rights.`);
            }
        },
        async revokeAdminRights(user) {
            try {
                await axios.post(`/admin/manage-admin/`, {
                    username: user.username
                });
                this.$toast.success(`Successfully revoked admin rights to ${user.username}.`);
                this.adminManagementInfo = { user: null, action: '' };
                this.fetchUsers('/api/v1/users/');
            } catch (error) {
                this.$toast.error(`Something went wrong during revoking admin rights.`);
            }
        },
        badgeText(user) {
            if (user.is_superuser) {
                return "Superuser";
            } else if (user.is_staff) {
                return "Admin";
            }
        },
        setAdminModalInfo(user,action){
            this.adminManagementInfo = {
                user: user,
                action: action
            };
        },
        manageActionType(user,action){
            if (action === 'Revoke'){
                this.revokeAdminRights(user);
            } else {
                this.grantAdminRights(user);
            }
        }
    }
}
</script>


<style scoped>
.user-card.horizontal {
    background: #E9F1FA;
    display: flex;
    align-items: center;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    border-left: 4px solid #3a6f8f;
}

.content {
    flex-grow: 1;
}

.user-name {
    color: #333;
    margin-bottom: 0.25rem;
}

.expanded-section {
    padding-top: 1rem;
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
}</style>