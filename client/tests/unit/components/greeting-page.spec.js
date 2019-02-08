import { shallowMount } from '@vue/test-utils'

import GreetingPage from '@/components/greeting-page.vue'

describe('GreetingPage', () => {
  const factory = (propsData) => {
    return shallowMount(GreetingPage, {
      sync: false,
      propsData: {
        ...propsData
      }
    })
  }

  it('displays the messages correctly', () => {
    const props = {
      label: 'Welcome',
      helpText: 'We are here to help you'
    }
    const wrapper = factory(props)

    const labelAppName = wrapper.find('p[data-ref=app-name]')
    expect(labelAppName.isVisible()).toBeTruthy()
    expect(labelAppName.text()).toEqual('globals.app-name')

    const labelElement = wrapper.find('p[data-ref=greeting-label]')
    expect(labelElement.isVisible()).toBeTruthy()
    expect(labelElement.text()).toEqual(props.label)

    const helpTextElement = wrapper.find('p[data-ref=help-text]')
    expect(helpTextElement.isVisible()).toBeTruthy()
    expect(helpTextElement.text()).toEqual(props.helpText)
  })

  it('hides the helpText when it is not passed', () => {
    const wrapper = factory({
      label: 'Welcome'
    })

    expect(wrapper.find('p[data-ref=help-text]').exists()).toBeFalsy()
  })
})
