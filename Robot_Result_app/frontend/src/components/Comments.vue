<template>
    <div class="container mt-4 bg-light p-4 ">
        <span class="fw-bold">Comments</span>
        <!-- Comments Display Section -->
        <div class="comments-display" @scroll="checkScroll">
            <div v-for="comment in comments" :key="comment.id" class="mb-4">
                <div class="card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <h6 class="fw-bold mb-1">{{ comment.author }}</h6>
                            <small class="text-muted">{{ formatDate(comment.updated_at) }}</small>
                        </div>
                        <p v-if="!isEditing(comment.id)" class="mt-2">{{ comment.text }}</p>
                        <textarea v-else class="form-control mb-2" v-model="editText" rows="3" maxlength="200"></textarea>
                        <div class="d-flex justify-content-end">
                            <button v-if="comment.canEdit" class="btn btn-link hover-zoom-icon"
                                @click="toggleEdit(comment)">
                                <font-awesome-icon
                                    :icon="this.editingCommentId === comment.id ? 'fa-solid fa-floppy-disk' : 'fa-solid fa-pencil'"
                                    style="color: #3a6d8d;" />
                            </button>
                            <button v-if="comment.canEdit" class="btn btn-link text-danger hover-zoom-icon"
                                @click="deleteComment(comment.id)">
                                <font-awesome-icon icon="fa-solid fa-trash" style="color: #bf1d1d;" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Add Comment Section -->
        <div class="mt-4">
            <textarea class="form-control" v-model="newCommentText" placeholder="Write a comment..." rows="3" maxlength="200"></textarea>
            <button class="btn bg-ucla-blue clickable-item text-seasalt btn-sm mt-2" id="post-comment" @click="addComment">Post</button>
        </div>
    </div>
</template>


<script>
import { axios } from "@/common/api.service.js";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

export default {
    name: "CommentsComponent",
    props: ['teamId', 'testRunId'],
    data() {
        return {
            comments: {},
            pagination: {},
            editingCommentId: null,
            editText: '',
            newCommentText: '',
            loading: false,
            maxComments: 20, // Maximum number of comments to display at once
        };
    },
    created() {
        this.loadComments();
    },
    methods: {
        extractPath(url) {
            if (!url) return null;
            const basePath = '/api/v1/';
            const index = url.indexOf(basePath);
            return index !== -1 ? url.substring(index) : null;
        },
        async loadComments(url = `/api/v1/teams/${this.teamId}/test-runs/${this.testRunId}/comments/`) {
            this.loading = true;
            try {
                const response = await axios.get(url);
                let currentUser = await this.getCurrentUser();
                this.comments = response.data.results.map(comment => ({
                    ...comment,
                    canEdit: comment.author === currentUser
                }));
                let next = this.extractPath(response.data.next);
                let prev = this.extractPath(response.data.previous);
                this.pagination = {
                    next: next,
                    previous: prev
                };
            }
            catch (error) {
                this.$toast.error(`Error loading comments.`);
            }
            finally {
                this.loading = false;
            }
        },
        async getCurrentUser() {
            try {
                const user = await axios.get('/auth/users/me/');
                return user.data.username;
            }
            catch (error) {
                this.$toast.error(`Error fetching current user.`);
            }
        },
        isEditing(commentId) {
            return this.editingCommentId === commentId;
        },
        toggleEdit(comment) {
            if (this.isEditing(comment.id)) {
                this.saveComment(comment);
            }
            else {
                this.editingCommentId = comment.id;
                this.editText = comment.text;
            }
        },
        async saveComment(comment) {
            try {
                await axios.put(`/api/v1/teams/${this.teamId}/test-runs/${this.testRunId}/comments/${comment.id}/`, {
                    text: this.editText
                });
            }
            catch (error) {
                this.$toast.error(`Error saving comment.`);
            } finally{
                this.editingCommentId = null;
                this.loadComments();
            }

        },
        async deleteComment(commentId) {
            try {
                await axios.delete(`/api/v1/teams/${this.teamId}/test-runs/${this.testRunId}/comments/${commentId}/`);
            }
            catch (error) {
                this.$toast.error(`Error deleting comment.`);
            } finally{
                this.loadComments();
            }
        },
        async addComment() {
            if (!this.newCommentText.trim()) {
                alert('Comment cannot be empty.');
                return;
            }
            try {
                await axios.post(`/api/v1/teams/${this.teamId}/test-runs/${this.testRunId}/comments/`, {
                    text: this.newCommentText,
                    testrun: this.testRunId
                });
                this.newCommentText = '';
                this.loadComments();
            }
            catch (error) {
                this.$toast.error(`Error adding comment.`);
            }
        },
        formatDate(dateString) {
            const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false };
            return new Date(dateString).toLocaleString('default', options);
        },
        async loadMoreComments(url, prepend = false) {
            if (!url || this.loading)
                return;
            this.loading = true;
            try {
                const response = await axios.get(url);
                let currentUser = await this.getCurrentUser();
                let newComments = response.data.results.map(comment => ({
                    ...comment,
                    canEdit: comment.author === currentUser
                }));
                // Filter out duplicate comments
                newComments = newComments.filter(newComment => !this.comments.some(comment => comment.id === newComment.id));
                if (prepend) {
                    this.comments = [...newComments, ...this.comments].slice(0, this.maxComments);
                }
                else {
                    this.comments = [...this.comments, ...newComments].slice(-this.maxComments);
                }
                this.pagination = {
                    next: response.data.next,
                    previous: response.data.previous
                };
            }
            catch (error) {
                this.$toast.error(`Error loading more comments.`);
            }
            finally {
                this.loading = false;
            }
        },
        checkScroll(event) {
            const container = event.target;
            const nearBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 100;
            const nearTop = container.scrollTop < 100;
            if (nearBottom) {
                this.loadMoreComments(this.pagination.next);
            }
            if (nearTop) {
                this.loadMoreComments(this.pagination.previous, true);
            }
        },
    },
    components: { FontAwesomeIcon }
};
</script>
  
<style scoped>
.comments-display {
    max-height: 100vh;
    /* Adjust based on your layout */
    overflow-y: auto;
    overflow-x: hidden;
    padding-bottom: 20px;
}

.hover-zoom-icon {
    transition: transform 0.3s ease;
}

.hover-zoom-icon:hover {
    transform: scale(1.1);
}
</style>
  