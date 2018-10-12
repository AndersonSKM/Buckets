import axios from 'axios'

const jsonApi = axios.create({
  baseURL: process.env.VUE_APP_API_URL
})

export default jsonApi
