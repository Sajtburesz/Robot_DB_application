import { shallowMount } from '@vue/test-utils';
import RetreiveTestRun from '@/components/RetreiveTestRun.vue';
import FontAwesomeIcon from '@fortawesome/vue-fontawesome';
const mockToast = {
    error: jest.fn(),
    success: jest.fn()
  };

describe('RetreiveTestRun', () => {
  let wrapper;

  const testRunMock = {
    id: 1,
    status: 'PASS',
    executed_at: new Date().toISOString(),
    attributes: {},
    suites: {
      suites: [],
      next: null,
      previous: null
    }
  };

  beforeEach(() => {
    wrapper = shallowMount(RetreiveTestRun, {
      propsData: {
        testRunId: '1',
        teamId: 'team123',
      },
      data() {
        return {
          testRun: testRunMock,
          showTestRunDetails: false,
          editMode: false,
        };
      },
      global: {
        mocks:{
            $toast: mockToast
        },
        stubs: {
            FontAwesomeIcon: true, 
          },
        components: {
          FontAwesomeIcon
        }
      }
    });
  });

  it('renders test run details header', () => {
    const header = wrapper.find('.detailes-header');
    expect(header.exists()).toBeTruthy();
    expect(header.text()).toContain(`#${testRunMock.id} Test Run Details`);
  });

  it('renders status badge correctly', () => {
    const badge = wrapper.find('.badge');
    expect(badge.exists()).toBeTruthy();
    expect(badge.text()).toBe(testRunMock.status);
    expect(badge.classes()).toContain('badge-success');
  });

  it('toggles test run details on button click', async () => {
    const toggleButton = wrapper.find('.btn-link');
    await toggleButton.trigger('click');
    expect(wrapper.vm.showTestRunDetails).toBe(true);
    const cardBody = wrapper.find('.card-body');
    expect(cardBody.exists()).toBeTruthy();
  });

  it('renders suites list when test run details are shown', async () => {
    wrapper.setData({ showTestRunDetails: true });
    await wrapper.vm.$nextTick();
    const suiteCards = wrapper.findAll('.card.mb-4');
    expect(suiteCards.length).toBe(1);
  });

});
