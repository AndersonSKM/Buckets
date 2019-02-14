const ApiValidationsHandlerMixin = {
  methods: {
    handleApiValidations: (error, validator) => {
      validator.errors.clear()

      if (!error.hasOwnProperty('response')) {
        return
      }

      const response = error.response
      if (response.status >= 400 && response.status < 500) {
        if (!response.hasOwnProperty('data')) {
          return
        }

        Object.keys(response.data).forEach((key) => {
          if (!(response.data[key] instanceof Array)) {
            return
          }

          response.data[key].forEach((errorMessage) => {
            validator.errors.add({
              field: key,
              msg: errorMessage
            })
          })
        })
      }
    }
  }
}

export default ApiValidationsHandlerMixin
