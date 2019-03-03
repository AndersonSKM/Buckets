import { shallowMount } from '@vue/test-utils'

import SignInReference from '@/components/sign-in-reference.vue'

describe('SignInReference', () => {
  const factory = (propsData) => {
    return shallowMount(SignInReference, {
      sync: false,
      propsData: {
        ...propsData
      },
      stubs: [
        'router-link'
      ]
    })
  }

  it('renders correctly', () => {
    const props = {
      label: 'Are you ready?'
    }
    const wrapper = factory(props)

    const labelElement = wrapper.find('p[data-ref=sign-in-reference-label]')
    expect(labelElement.isVisible()).toBeTruthy()
    expect(labelElement.text()).toContain(props.label)

    const linkElement = wrapper.find('router-link-stub')
    expect(linkElement.isVisible()).toBeTruthy()
    expect(linkElement.attributes('to')).toEqual('/sign-in')

    const linkLabelElement = wrapper.find('u')
    expect(linkLabelElement.isVisible()).toBeTruthy()
    expect(linkLabelElement.text()).toEqual('sign-in-view.label')
  })
})
