import { http} from '@/utils/http'

function normalize(space) {
  return {
    ...space,
    price: Number(space.price ?? 0),
    rating: Number(space.rating ?? 0),
    downloads: Number(space.downloads ?? 0),
    reviews: Number(space.reviews ?? 0),
    // publishedAt 后端为 "YYYY-MM-DD"，目前仅展示，保留字符串即可
  }
}

export async function getSpace() {
  // 由于响应拦截器已解包，get('/workspace') 所以 url 对应base_url + '/workspace',这个url要和后端 urls.py中定义的名字相对应
  const list = await http.get('/workspace')
  return (Array.isArray(list) ? list : []).map(normalize)
}
