<template>
  <div class="container mt-4 bg-light p-4 border rounded">
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
            <input v-else type="text" v-model="editText" class="form-control mb-2">
            <div class="d-flex justify-content-end">
              <button v-if="comment.canEdit" class="btn btn-link hover-zoom-icon" @click="toggleEdit(comment)">
                <font-awesome-icon :icon="this.editingCommentId === comment.id ? 'fa-solid fa-floppy-disk' : 'fa-solid fa-pencil'" style="color: #3a6d8d;" />
              </button>
              <button v-if="comment.canEdit" class="btn btn-link text-danger hover-zoom-icon" @click="confirmDelete(comment.id)">
                <font-awesome-icon icon="fa-solid fa-trash" style="color: #bf1d1d;"/>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Comment Section -->
    <div class="mt-4">
      <textarea class="form-control" v-model="newCommentText" placeholder="Write a comment..." rows="3"></textarea>
      <button class="btn btn-success btn-sm mt-2" @click="addComment">Post</button>
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
        async loadComments(url = `/api/v1/teams/${this.teamId}/test-runs/${this.testRunId}/comments/`) {
            this.loading = true;
            try {
                const response = await axios.get(url);
                let currentUser = await this.getCurrentUser();
                this.comments = response.data.results.map(comment => ({
                    ...comment,
                    canEdit: comment.author === currentUser
                }));
                this.pagination = {
                    next: response.data.next,
                    previous: response.data.previous
                };
            }
            catch (error) {
                console.error('Error loading comments:', error);
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
                console.error('Error fetching current user:', error);
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
                await this.loadComments();
            }
            catch (error) {
                console.error('Error saving comment:', error);
            }
            this.editingCommentId = null;
        },
        confirmDelete(commentId) {
            if (confirm('Are you sure you want to delete this comment?')) {
                this.deleteComment(commentId);
            }
        },
        async deleteComment(commentId) {
            try {
                await axios.delete(`/api/v1/teams/${this.teamId}/test-runs/${this.testRunId}/comments/${commentId}/`);
                await this.loadComments();
            }
            catch (error) {
                console.error('Error deleting comment:', error);
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
                await this.loadComments();
            }
            catch (error) {
                console.error('Error adding comment:', error);
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
                console.error('Error loading more comments:', error);
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
  max-height: 80vh;
  /* Adjust based on your layout */
  overflow-y: auto;
  overflow-x: hidden;
  padding-bottom: 20px;
}

.add-comment-section {
  padding: 10px;
}

.comment {
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 5px;
}

.author {
  font-weight: bold;
}

.timestamp {
  font-size: 0.8rem;
  color: #666;
}

.comment-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.hover-zoom-icon {
    transition: transform 0.3s ease;
  }
  
.hover-zoom-icon:hover {
transform: scale(1.1);
}
</style>
  