import { mount } from '@vue/test-utils'
import flushPromises from 'flush-promises'

import SignInView from '@/views/sign-in.vue'

describe('SignInView', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(SignInView, {
      sync: false,
      stubs: [
        'router-link',
        'cmp-greeting-page'
      ]
    })

    wrapper.setData({
      email: 'test@test.com',
      password: 'password'
    })
  })

  afterEach(() => {
    wrapper.vm.$router.push.mockClear()
    wrapper.vm.$store.dispatch.mockClear()
  })

  it('does not call the store if email and password are blank', async () => {
    wrapper.setData({
      email: '',
      password: ''
    })
    wrapper.setMethods({
      resetForm: jest.fn()
    })
    wrapper.find('form[data-ref=form]').trigger('submit')
    await flushPromises()

    expect(wrapper.vm.errors.count()).toBe(2)
    expect(wrapper.vm.$store.dispatch).toHaveBeenCalledTimes(0)
    expect(wrapper.vm.resetForm).toHaveBeenCalledTimes(0)
  })

  it('calls the store if email and password are not blank', async () => {
    wrapper.setMethods({
      resetForm: jest.fn()
    })
    wrapper.vm.$store.dispatch = jest.fn(() => {
      return new Promise((resolve, reject) => {
        resolve({
          status: 200
        })
      })
    })
    wrapper.find('form[data-ref=form]').trigger('submit')
    await flushPromises()

    expect(wrapper.vm.$store.dispatch).toHaveBeenCalledWith('auth/obtainToken', {
      email: wrapper.vm.email,
      password: wrapper.vm.password
    })
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/')
    expect(wrapper.vm.resetForm).toHaveBeenCalledTimes(1)
  })

  it('sets the error message if api return a 400 error', async () => {
    wrapper.setMethods({
      resetForm: jest.fn()
    })
    wrapper.vm.$store.dispatch = jest.fn(() => {
      return new Promise((resolve, reject) => {
        const error = new Error('Bad Request')
        error.response = {
          status: 400,
          data: {
            non_field_errors: [
              'Error!'
            ]
          }
        }
        reject(error)
      })
    })
    wrapper.find('form[data-ref=form]').trigger('submit')
    await flushPromises()

    expect(wrapper.vm.$router.push).toHaveBeenCalledTimes(0)
    expect(wrapper.vm.resetForm).toHaveBeenCalledTimes(1)
    expect(wrapper.vm.$validator.errors.count()).toEqual(1)
  })

  it('clears the form and focus on email field when called', () => {
    wrapper.setData({
      email: 'test@test.com',
      password: 'test'
    })
    wrapper.vm.$refs.email.focus = jest.fn()
    wrapper.vm.resetForm()

    expect(wrapper.vm.email).toBeUndefined()
    expect(wrapper.vm.password).toBeUndefined()
    expect(wrapper.vm.$refs.email.focus).toHaveBeenCalledTimes(1)
  })
})
