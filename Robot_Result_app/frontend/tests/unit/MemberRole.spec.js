import { shallowMount } from '@vue/test-utils';
import MemberRoleComponent from '@/components/MemberRole.vue';

describe('MemberRoleComponent', () => {
  let wrapper;
  const roles = ['Member', 'Maintainer'];
  const member = { id: 1, name: 'John Doe', role: 'Member' };

  beforeEach(() => {
    wrapper = shallowMount(MemberRoleComponent, {
      propsData: {
        roles: roles,
        member: member
      }
    });
  });

  it('renders a select element', () => {
    expect(wrapper.find('select').exists()).toBe(true);
  });

  it('renders the correct number of role options', () => {
    const options = wrapper.findAll('option');
    expect(options.length).toBe(roles.length);
  });

  it('renders each role as an option', () => {
    const options = wrapper.findAll('option');
    roles.forEach((role, index) => {
      expect(options.at(index).text()).toBe(role);
    });
  });

  it('sets the initial selected role based on the member prop', () => {
    const selectedOption = wrapper.find('select').element.value;
    expect(selectedOption).toBe(member.role);
  });

  it('emits "role-changed" event with new role when selection changes', async () => {
    const newRole = 'Admin';
    await wrapper.setData({ localRole: newRole });
    expect(wrapper.emitted('role-changed')).toBeTruthy();
    expect(wrapper.emitted('role-changed')[0]).toEqual([{ member: member, newRole: newRole }]);
  });

});
