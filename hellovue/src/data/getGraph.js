import { http} from '@/utils/http'

function normalize(graph) {
  return {
    ...graph,
    price: Number(graph.price ?? 0),
    rating: Number(graph.rating ?? 0),
    downloads: Number(graph.downloads ?? 0),
    reviews: Number(graph.reviews ?? 0),
    // publishedAt 后端为 "YYYY-MM-DD"，目前仅展示，保留字符串即可
  }
}

export async function getGraph() {
  const list = await http.get('/graph')
  return (Array.isArray(list) ? list : []).map(normalize)
}
