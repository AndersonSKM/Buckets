import jwt from 'jsonwebtoken'
import API from '@/plugins/api.js'

class AuthService {
  static async createToken (credentials) {
    return API.post('api/auth/jwt/create/', credentials)
  }

  static async refreshToken (oldToken) {
    let newToken = ''

    try {
      const response = await API.post('api/auth/jwt/refresh/', { token: oldToken })
      if (response.status === 200) {
        newToken = response.data.token
      }
    } catch {
    }

    return newToken
  }

  static canRefreshToken (encodedToken) {
    if (this.isExpiredToken(encodedToken)) {
      return false
    }

    const token = this.decodedToken(encodedToken)
    const oneMinuteInMilliseconds = 60000
    const oneHourInMilliseconds = 36e5

    const tokenWasCreatedWithinFourHours = (Math.abs(Date.now() - token.orig_iat) / oneHourInMilliseconds) <= 4
    const tokenHasMoreThanThirteenMinutes = (Math.abs(Date.now() - token.orig_iat) / oneMinuteInMilliseconds) >= 13
    return tokenWasCreatedWithinFourHours && tokenHasMoreThanThirteenMinutes
  }

  static isExpiredToken (encodedToken) {
    const token = this.decodedToken(encodedToken)
    if (!token) {
      return true
    }

    return Date.now() > token.exp
  }

  static decodedToken (encodedToken) {
    if (!encodedToken) {
      return ''
    }

    const decodedObject = jwt.decode(encodedToken)
    return {
      ...decodedObject,
      orig_iat: decodedObject.orig_iat * 1000,
      exp: decodedObject.exp * 1000
    }
  }
}

export default AuthService
