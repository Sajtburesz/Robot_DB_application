<template>
    <div class="vh-100 my-5">
        <div class="container">
            <div class="row">
                <!-- Left Side Menu -->
                <div class="col-md-2 border-end border-2">
                    <LeftSideAdminMenu />
                </div>

                <!-- Manage Attribute Form -->
                <div class="col-md-10 ps-5 d-flex align-items-center">
                    <div class="w-50">
                        <!-- Attributes Wrapper -->
                        <div v-for="(attribute, index) in attributes" :key="index" class="mb-3 position-relative">
                            <!-- Attribute Input and Buttons -->
                            <div class="d-flex align-items-center">
                                <input type="text" class="form-control text-center-input rounded-pill rounded-3"
                                    style="text-align: center;" v-model="attribute.key_name"
                                    @input="attribute.isNew || checkForChange(attribute, index)" required>
                                <button v-if="attribute.isNew || attribute.isModified" type="button"
                                    class="btn btn-link hover-zoom-icon ms-2" @click="saveAttribute(index)"
                                    :disabled="!attribute.key_name.trim()">
                                    <font-awesome-icon icon="fa-solid fa-floppy-disk" />
                                </button>
                                <button type="button" class="btn btn-link hover-zoom-icon ms-2" data-bs-toggle="modal" data-bs-target="#attributeDeleteModal" @click="deleteIndex = index">
                                    <font-awesome-icon icon="fa-solid fa-trash" style="color: red;" />
                                </button>
                            </div>
                        </div>
                        <!-- Plus Button in the Middle -->
                        <div class="position-absolute"
                            style="left: 39%; transform: translateX(-50%);">
                            <button type="button" class="btn btn-link hover-zoom-icon" @click="addAttribute()">
                               <font-awesome-icon icon="fa-solid fa-circle-plus" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Delete Confirmation Modal -->
        <div class="modal fade" tabindex="-1" role="dialog" aria-hidden="true" id="attributeDeleteModal">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Delete Attribute</h5>
                        <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <p>Are you sure about deleting this attribute?</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
                        <button type="button" class="btn btn-danger" @click="deleteAttribute()"
                            data-bs-dismiss="modal">Yes</button>
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
    components: {
        LeftSideAdminMenu,
    },
    data() {
        return {
            attributes: [],
            deleteIndex: null
        };
    },
    async mounted() {
        await this.fetchAttributes();
        this.deleteIndex = null;
        if (this.attributes.length === 0){
            this.addAttribute();
        }
    },
    methods: {
        async fetchAttributes() {
            try {
                this.attributes = [];

                const response = await axios.get(`/api/v1/attributes/`);
                this.attributes = response.data.results.map(attr => ({
                    ...attr,
                    isNew: false,
                    isModified: false,
                    originalName: attr.key_name
                }));
            } catch (error) {
                this.$toast.error(`Error fetching attributes: ${error}`);
            }
        },
        addAttribute() {
            this.attributes.push({ key_name: '', isNew: true, isModified: false });
        },
        checkForChange(attribute, index) {
            attribute.isModified = attribute.key_name !== this.attributes[index].originalName;
        },
        async deleteAttribute() {

            try {
                if (this.attributes[this.deleteIndex].isNew === false){
                    await axios.delete(`/api/v1/attributes/${this.attributes[this.deleteIndex].id}/`);
                    this.deleteIndex = null;
                    await this.fetchAttributes();
                    this.$toast.success(`Successfully deleted attribute.`)
                } else {
                    this.attributes.splice(this.deleteIndex, 1);
                    this.deleteIndex = null;
                }
            } catch (error) {
                this.$toast.error(`Something went wrong while deleting attribute. Please contact sysadmin.`);
            }
        },
        async saveAttribute(index) {
            const attribute = this.attributes[index];
            if (attribute.key_name.trim() && (attribute.isNew || attribute.isModified)) {
                try{   
                    if (attribute.isNew === false){
                        await axios.put(`/api/v1/attributes/${attribute.id}/`,{key_name: attribute.key_name});

                        this.$toast.success(`Successfully updated attribute ${attribute.key_name}.`);

                        await this.fetchAttributes();
                    } else {
                        await axios.post(`/api/v1/attributes/create/`,{key_name: attribute.key_name});

                        this.$toast.success(`Successfully created attribute ${attribute.key_name}.`);

                        await this.fetchAttributes();
                    }
                } catch (error){
                    this.$toast.error(`Something went wrong while creating new attribute`);
                }
            }
        },
    }
};
</script>

<style scoped>
.hover-zoom-icon {
    transition: transform 0.3s ease;
}

.hover-zoom-icon:hover {
    transform: scale(1.1);
}
</style>
