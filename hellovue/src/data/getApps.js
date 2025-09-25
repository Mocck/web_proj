import { apps as mock } from '@/mock/apps'
import { http, USE_MOCK } from '@/utils/http'

function normalize(app) {
  return {
    ...app,
    price: Number(app.price ?? 0),
    rating: Number(app.rating ?? 0),
    downloads: Number(app.downloads ?? 0),
    reviews: Number(app.reviews ?? 0),
    // publishedAt 后端为 "YYYY-MM-DD"，目前仅展示，保留字符串即可
  }
}

export async function getApps() {
  if (USE_MOCK) return mock.map(normalize)

  // 由于响应拦截器已解包，get('/apps') 直接返回后端的 data（数组）
  const list = await http.get('/apps')
  return (Array.isArray(list) ? list : []).map(normalize)
}
