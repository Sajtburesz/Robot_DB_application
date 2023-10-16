<template>
    <div>
        <select v-model="localRole">
            <option v-for="role in roles" :key="role" :value="role">{{ role }}</option>
        </select>
    </div>
</template>

<script>
export default {
    name: 'MemberRoleComponent',
    props: ['roles','member'],
    data() {
        return {
            localRole: this.member.role
        };
    },
    watch: {
        localRole(newValue, oldValue) {
            if (newValue !== oldValue) {
                this.$emit('role-changed', { member: this.member, newRole: newValue });
            }
        }
    }
}
</script>
