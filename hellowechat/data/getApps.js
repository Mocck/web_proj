const { apps: mock } = require('../mock/apps')
const { get } = require('../utils/http')
const { getUseMock } = require('../utils/env')

function normalize(app) {
  return Object.assign({}, app, {
    price: Number(app.price || 0),
    rating: Number(app.rating || 0),
    downloads: Number(app.downloads || 0),
    reviews: Number(app.reviews || 0)
  })
}

async function getApps() {
  if (getUseMock()) return mock.map(normalize)
  const list = await get('/apps')
  return (Array.isArray(list) ? list : []).map(normalize)
}

module.exports = { getApps }
