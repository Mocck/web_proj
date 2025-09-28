const { BASE_API } = require('../config/index')

function request(method, url, { data, headers } = {}) {
  return new Promise((resolve, reject) => {
    wx.request({
      method,
      url: url.startsWith('http') ? url : `${BASE_API}${url}`,
      data,
      header: Object.assign({
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }, headers || {}),
      success(res) {
        const ct = res.header && (res.header['content-type'] || res.header['Content-Type'] || '')
        if (ct && ct.includes('octet-stream')) return resolve(res.data)

        const payload = res.data
        if (payload && typeof payload === 'object' && 'code' in payload && 'data' in payload) {
          if (payload.code === 0) return resolve(payload.data)
          const err = new Error(payload.message || '业务失败'); err.code = payload.code
          return reject(err)
        }
        return resolve(payload) // 兜底
      },
      fail(e) { reject(new Error(e.errMsg || '网络不可用或服务器无响应')) }
    })
  })
}

module.exports = {
  get: (url, opts) => request('GET', url, opts),
  post: (url, opts) => request('POST', url, opts),
  request
}
