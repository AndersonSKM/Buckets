import { shallow } from '@vue/test-utils'

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
    wrapper = shallow(SignIn, {
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
    wrapper.setMethods({
      resetForm: jest.fn()
    })
    wrapper.find('form').trigger('submit')
    await flushPromises()

    expect(wrapper.vm.errors.count()).toBe(2)
    expect(mockStore.dispatch).toHaveBeenCalledTimes(0)
    expect(wrapper.vm.resetForm).toHaveBeenCalledTimes(0)
  })

  it("calls the store if email and password aren't blank", async () => {
    wrapper.setMethods({
      resetForm: jest.fn()
    })
    wrapper.find('form').trigger('submit')
    await flushPromises()

    expect(wrapper.vm.$store.dispatch).toHaveBeenCalledWith('auth/obtainToken', {
      email: wrapper.vm.email,
      password: wrapper.vm.password
    })
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/home')
    expect(wrapper.vm.form_errors).toEqual([])
    expect(wrapper.vm.resetForm).toHaveBeenCalledTimes(1)
  })

  it('sets the error message if api return a 400 error', async () => {
    wrapper.setMethods({
      resetForm: jest.fn()
    })
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
    wrapper.find('form').trigger('submit')
    await flushPromises()

    expect(wrapper.vm.$router.push).toHaveBeenCalledTimes(0)
    expect(wrapper.vm.form_errors).toEqual(['Error!'])
    expect(global.console.log).toHaveBeenCalled()
    expect(wrapper.vm.resetForm).toHaveBeenCalledTimes(1)
  })

  it('clears the form and focus on email field when called', async () => {
    wrapper.setData({
      email: 'test@test.com',
      password: 'test',
      form_errors: ['error']
    })
    wrapper.vm.resetForm()
    await flushPromises()

    expect(wrapper.find('input[data-ref=email]').attributes('focused')).toBeTruthy()
    expect(wrapper.vm.email).toBeUndefined()
    expect(wrapper.vm.password).toBeUndefined()
    expect(wrapper.vm.form_errors).toEqual(['error'])
  })
})
