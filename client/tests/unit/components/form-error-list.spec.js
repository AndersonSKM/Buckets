import { shallowMount } from '@vue/test-utils'
import flushPromises from 'flush-promises'

import FormErrorList from '@/components/form-error-list.vue'

describe('FormErrorList', () => {
  let wrapper

  beforeEach(() => {
    wrapper = shallowMount(FormErrorList, {
      sync: false
    })
  })

  it('displays the errors correctly', async () => {
    wrapper.vm.$validator.errors.add({ field: 'Name', msg: 'Invalid Name' })
    wrapper.vm.$validator.errors.add({ field: 'non_field_errors', msg: 'Invalid User' })
    wrapper.vm.$validator.errors.add({ field: 'non_field_errors', msg: 'Invalid Password' })
    await flushPromises()

    let errorList = wrapper.findAll('li')
    expect(errorList.length).toEqual(2)
    expect(errorList.at(0).text()).toEqual('Invalid User')
    expect(errorList.at(1).text()).toEqual('Invalid Password')
  })
})
