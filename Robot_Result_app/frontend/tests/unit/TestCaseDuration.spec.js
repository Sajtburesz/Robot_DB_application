import { shallowMount } from '@vue/test-utils';
import TestCaseDuration from '@/components/TestCaseDuration.vue';
const mockToast = {
    error: jest.fn(),
    success: jest.fn()
  };
describe('TestCaseDuration', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(TestCaseDuration, {
        data() {
            return {
              selectedTeam: 'team123',
              selectedTeamName: 'Team 123',
              teams: [{ id: 'team123', name: 'Team 123' }],
              selectedSuite: null,
              suites: ['Suite 1', 'Suite 2'],
              chartSeries: [], 
              loaded: true,
            };
          },
        global: {
            mocks:{
                $toast: mockToast
            },
          }

    });
  });

  it('renders team and suite dropdowns', () => {
    const teamDropdown = wrapper.find('#team-dropdown');
    const suiteDropdown = wrapper.find('#suite-dropdown');
    expect(teamDropdown.exists()).toBe(true);
    expect(suiteDropdown.exists()).toBe(true);
  });

  it('displays default text in dropdowns', () => {
    const teamDropdownText = wrapper.find('#team-dropdown').text();
    const suiteDropdownText = wrapper.find('#suite-dropdown').text();
    
    expect(teamDropdownText).toContain('Team 123');
    expect(suiteDropdownText).toContain('Select a suite');
  });

  it('shows chart placeholder initially', () => {
    const chartPlaceholder = wrapper.find('.no-data-message');
    expect(chartPlaceholder.exists()).toBe(true);
    expect(chartPlaceholder.text()).toContain('No');
  });

});
