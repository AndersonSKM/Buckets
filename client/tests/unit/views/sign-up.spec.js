import { mount } from '@vue/test-utils'
import flushPromises from 'flush-promises'

import SignUpView from '@/views/sign-up.vue'

describe('SignUpView', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(SignUpView, {
      sync: false,
      stubs: [
        'router-link'
      ],
      mocks: {
        $services: {
          user: {
            create: jest.fn()
          }
        }
      }
    })

    wrapper.setData({
      ok: false,
      name: 'John Doe',
      email: 'test@test.com',
      password: 'password'
    })
  })

  afterEach(() => {
    wrapper.vm.$services.user.create.mockClear()
  })

  describe('Submit', () => {
    it('does nothing if form fields is blank', async () => {
      wrapper.setData({
        name: '',
        email: '',
        password: ''
      })
      wrapper.find('form[data-ref=form]').trigger('submit')
      await flushPromises()

      expect(wrapper.vm.errors.count()).toBe(3)
      expect(wrapper.vm.$services.user.create).not.toHaveBeenCalled()
    })

    it('calls the store if email and password are not blank', async () => {
      wrapper.vm.$services.user.create = jest.fn(() => {
        return new Promise((resolve) => {
          resolve({
            status: 201
          })
        })
      })
      wrapper.find('form[data-ref=form]').trigger('submit')
      await flushPromises()

      expect(wrapper.vm.$services.user.create).toHaveBeenCalledWith({
        name: wrapper.vm.name,
        email: wrapper.vm.email,
        password: wrapper.vm.password
      })
      expect(wrapper.vm.ok).toBeTruthy()
    })

    it('sets the error message if api return a 400 error', async () => {
      wrapper.vm.$services.user.create = jest.fn(() => {
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

      expect(wrapper.vm.ok).toBeFalsy()
      expect(wrapper.vm.$validator.errors.count()).toEqual(1)
      expect(wrapper.vm.password).toBe('')
    })
  })
})
