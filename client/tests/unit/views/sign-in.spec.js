import { mount } from '@vue/test-utils'

import flushPromises from 'flush-promises'

import SignIn from '@/views/sign-in.vue'

describe('sign-in.vue', () => {
  let wrapper
  let mockStore
  let mockRouter

  beforeEach(() => {
    mockRouter = {
      push: jest.fn()
    }
    mockStore = {
      dispatch: jest.fn(() => Promise.resolve())
    }
    wrapper = mount(SignIn, {
      sync: false,
      mocks: {
        $t: jest.fn(),
        $router: mockRouter,
        $store: mockStore
      }
    })

    wrapper.setData({
      email: 'test@test.com',
      password: 'password',
      form_errors: []
    })
  })

  it("doesn't call the store if email and password are blank", async () => {
    wrapper.setData({
      email: '',
      password: '',
      form_errors: []
    })
    wrapper.find('#btn-submit').trigger('click')
    await flushPromises()

    expect(wrapper.vm.errors.count()).toBe(2)
    expect(mockStore.dispatch).toHaveBeenCalledTimes(0)
  })

  it("calls the store if email and password aren't blank", async () => {
    wrapper.find('#btn-submit').trigger('click')
    await flushPromises()

    expect(wrapper.vm.$store.dispatch).toHaveBeenCalledWith('auth/obtainToken', {
      email: wrapper.vm.email,
      password: wrapper.vm.password
    })
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/home')
    expect(wrapper.vm.form_errors).toEqual([])
  })

  it('sets the error message if api return a 400 error', async () => {
    global.console = {
      log: jest.fn()
    }
    mockStore.dispatch = jest.fn(() => {
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
    wrapper.find('#btn-submit').trigger('click')
    await flushPromises()

    expect(wrapper.vm.$router.push).toHaveBeenCalledTimes(0)
    expect(wrapper.vm.form_errors).toEqual(['Error!'])
    expect(global.console.log).toHaveBeenCalled()
  })
})
