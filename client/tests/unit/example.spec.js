import { shallowMount } from '@vue/test-utils'
import HelloWorld from '@/components/HelloWorld.vue'

describe('HelloWorld.vue', () => {
  it('renders vue component', () => {
    const wrapper = shallowMount(HelloWorld, {})
    expect(wrapper.classes()).toContain('bar')
  })
})
