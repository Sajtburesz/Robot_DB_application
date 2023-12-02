import { shallowMount } from '@vue/test-utils';
import CommentsComponent from '@/components/Comments.vue';

const mockToast = {
    error: jest.fn(),
    success: jest.fn()
  };

describe('CommentsComponent', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(CommentsComponent, {
        global: {
            mocks: {
              $toast: mockToast
            }
        },

      propsData: {
        teamId: 'team123',
        testRunId: 'testRun123',
      },
      data() {
        return {
          comments: [],
          newCommentText: '',
        };
      },
    });
  });

  it('renders without errors', () => {
    expect(wrapper.exists()).toBeTruthy();
  });

  it('adds new comment text to textarea', async () => {
    const textarea = wrapper.find('textarea');
    await textarea.setValue('New comment');
    expect(textarea.element.value).toBe('New comment');
  });

  it('shows post button', () => {
    const postButton = wrapper.find('#post-comment');
    expect(postButton.exists()).toBeTruthy();
  });

});

