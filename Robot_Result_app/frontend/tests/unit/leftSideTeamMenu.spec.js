import { mount } from '@vue/test-utils';
import LeftSideTeamMenu from '@/components/LeftSideTeamMenu.vue';
import { createRouter, createWebHistory, createMemoryHistory } from 'vue-router';

const routes = [
  { path: '/', redirect: '/teams/creat-team/' }, // Default route
  { path: '/teams/list/', name: 'ListTeamsView', component: {} },
  { path: '/teams/creat-team/', name: 'CreateTeamView', component: {} }
];
const router = createRouter({
  history: createMemoryHistory(), // Use memory history for tests
  routes,
});

describe('LeftSideTeamMenu', () => {
  let wrapper;

  beforeEach(async () => {
    router.push('/'); // Navigate to the default route
    await router.isReady(); // Wait for the router to be ready

    wrapper = mount(LeftSideTeamMenu, {
      global: {
        plugins: [router],
      },
    });
    await wrapper.vm.$nextTick();
  });
  it('renders without errors', () => {
    expect(wrapper.exists()).toBeTruthy();
  });

  it('has links to Manage Attributes and Manage Users',async () => {
    await wrapper.vm.$nextTick(); // Ensure all updates are processed
    const links = wrapper.findAll('a');
    expect(links.length).toBe(2); // Ensure there are two links

    // Check href of each link
    expect(links.at(0).attributes('href')).toBe('/teams/creat-team/');
    expect(links.at(1).attributes('href')).toBe('/teams/list/');

  });

});
