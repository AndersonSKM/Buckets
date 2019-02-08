import jwt from 'jsonwebtoken'
import API from '@/plugins/api.js'

class AuthService {
  async createToken (credentials) {
    return API.post('api/auth/jwt/create/', credentials)
  }

  async refreshToken (oldToken) {
    let newToken = ''

    try {
      const response = await API.post('api/auth/jwt/refresh/', { token: oldToken })
      if (response.status === 200) {
        newToken = response.data.token
      }
    } catch (error) {
      console.log('Failed to refresh token', error)
    }

    return newToken
  }

  canRefreshToken (encodedToken) {
    if (this.isExpiredToken(encodedToken)) {
      return false
    }

    const token = this.decodedToken(encodedToken)
    const oneMinuteInMiliseconds = 60000
    const oneHourInMiliseconds = 36e5

    const tokenWasCreatedWithinFourHours = (Math.abs(Date.now() - token.orig_iat) / oneHourInMiliseconds) <= 4
    const tokenHasMoreThanThirteenMinutes = (Math.abs(Date.now() - token.orig_iat) / oneMinuteInMiliseconds) >= 13
    return tokenWasCreatedWithinFourHours && tokenHasMoreThanThirteenMinutes
  }

  isExpiredToken (encodedToken) {
    const token = this.decodedToken(encodedToken)
    if (!token) {
      return true
    }

    return Date.now() > token.exp
  }

  decodedToken (encodedToken) {
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

export default new AuthService()
