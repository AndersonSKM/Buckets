import { mount } from '@vue/test-utils'
import flushPromises from 'flush-promises'

import PasswordResetView from '@/views/password-reset.vue'

describe('PasswordResetView', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(PasswordResetView, {
      sync: false,
      stubs: [
        'router-link'
      ],
      mocks: {
        $services: {
          user: {
            sendPasswordResetEmail: jest.fn(() => Promise.resolve({ status: 204 }))
          }
        }
      }
    })

    wrapper.setData({
      email: 'john.doe@test.com'
    })
  })

  afterEach(() => {
    wrapper.vm.$services.user.sendPasswordResetEmail.mockClear()
  })

  it('sets ok if form is submitted with a valid email', async () => {
    wrapper.find('form[data-ref=form]').trigger('submit')
    await flushPromises()

    expect(wrapper.vm.errors.count()).toBe(0)
    expect(wrapper.vm.$services.user.sendPasswordResetEmail).toHaveBeenCalledWith('john.doe@test.com')
    expect(wrapper.vm.ok).toBeTruthy()
  })

  it('does not set ok if api return an error', async () => {
    wrapper.vm.$services.user.sendPasswordResetEmail = jest.fn(() => {
      return new Promise((resolve, reject) => {
        const error = new Error('Bad Request')
        error.response = {
          status: 400,
          data: {
            email: [
              'E-mail does not exists'
            ]
          }
        }
        reject(error)
      })
    })
    wrapper.find('form[data-ref=form]').trigger('submit')
    await flushPromises()

    expect(wrapper.vm.errors.count()).toBe(1)
    expect(wrapper.vm.ok).toBeFalsy()
  })

  it('does nothing if the form is invalid', async () => {
    wrapper.setMethods({
      resetForm: jest.fn()
    })
    wrapper.setData({
      email: ''
    })
    wrapper.find('form[data-ref=form]').trigger('submit')
    await flushPromises()

    expect(wrapper.vm.errors.count()).toBe(1)
    expect(wrapper.vm.resetForm).toHaveBeenCalledTimes(1)
    expect(wrapper.vm.$services.user.sendPasswordResetEmail).not.toHaveBeenCalled()
  })

  it('returns the correct helpText when ok is false', () => {
    wrapper.setData({ ok: false })
    expect(wrapper.vm.helpText).toEqual('password-reset-view.help-text')
  })

  it('returns the correct helpText when ok is true', () => {
    wrapper.setData({ ok: true })
    expect(wrapper.vm.helpText).toBeNull()
  })

  it('shows the form when ok is false', async () => {
    wrapper.setData({ ok: true })
    await flushPromises()

    expect(wrapper.find('form[data-ref=form]').exists()).toBeFalsy()
    expect(wrapper.find('div[data-ref=try-sign-in]').exists()).toBeTruthy()
  })

  it('hides the form when ok is true', async () => {
    wrapper.setData({ ok: false })
    await flushPromises()

    expect(wrapper.find('form[data-ref=form]').exists()).toBeTruthy()
    expect(wrapper.find('div[data-ref=try-sign-in]').exists()).toBeFalsy()
  })
})
