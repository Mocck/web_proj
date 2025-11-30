import axios from 'axios'

export function ping() {
  return axios.get('http://localhost:8080/api/ping/')
}
