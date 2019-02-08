import ApiValidationsHandlerMixin from '@/mixins/api-validations-handler.js'

describe('handleApiValidations', () => {
  let mockValidator = {
    errors: {
      clear: jest.fn(),
      add: jest.fn()
    }
  }

  const handle = (response) => {
    const error = new Error('!')
    if (response) {
      error.response = response
    }

    ApiValidationsHandlerMixin.methods.handleApiValidations(error, mockValidator)
  }

  afterEach(() => {
    mockValidator.errors.clear.mockClear()
    mockValidator.errors.add.mockClear()
  })

  it('does anything if error does not have a response', () => {
    handle(null)

    expect(mockValidator.errors.clear).toHaveBeenCalledTimes(1)
    expect(mockValidator.errors.add).toHaveBeenCalledTimes(0)
  })

  it('does anything if response does not have data', () => {
    handle({
      status: 404
    })

    expect(mockValidator.errors.clear).toHaveBeenCalledTimes(1)
    expect(mockValidator.errors.add).toHaveBeenCalledTimes(0)
  })

  it('does anything if response status is greather than 499', () => {
    handle({
      status: 500
    })

    expect(mockValidator.errors.clear).toHaveBeenCalledTimes(1)
    expect(mockValidator.errors.add).toHaveBeenCalledTimes(0)
  })

  it('does anything if response status is less than 400', () => {
    handle({
      status: 303
    })

    expect(mockValidator.errors.clear).toHaveBeenCalledTimes(1)
    expect(mockValidator.errors.add).toHaveBeenCalledTimes(0)
  })

  it('does anything if validation message is not an array', () => {
    handle({
      status: 400,
      data: {
        field: 1
      }
    })

    expect(mockValidator.errors.clear).toHaveBeenCalledTimes(1)
    expect(mockValidator.errors.add).toHaveBeenCalledTimes(0)
  })

  it('calls add for each error in response data', () => {
    handle({
      status: 400,
      data: {
        email: [
          'First error',
          'Second error'
        ],
        password: [
          'Invalid'
        ]
      }
    })

    expect(mockValidator.errors.clear).toHaveBeenCalledTimes(1)
    expect(mockValidator.errors.add).toHaveBeenCalledTimes(3)
    expect(mockValidator.errors.add.mock.calls[0]).toEqual([{
      field: 'email',
      msg: 'First error'
    }])
    expect(mockValidator.errors.add.mock.calls[1]).toEqual([{
      field: 'email',
      msg: 'Second error'
    }])
    expect(mockValidator.errors.add.mock.calls[2]).toEqual([{
      field: 'password',
      msg: 'Invalid'
    }])
  })
})
