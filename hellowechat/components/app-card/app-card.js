Component({
  properties: {
    item: { type: Object, value: {} }
  },
  data: {
    stars: [0, 1, 2, 3, 4],
    starsOn: 0,        // 点亮的星数（四舍五入）
    scoreText: '0.0'   // 展示分，保留 1 位小数
  },
  observers: {
    'item.rating': function (r) {
      const n = parseFloat(r)
      const rating = isNaN(n) ? 0 : n
      const starsOn = Math.max(0, Math.min(5, Math.round(rating)))
      this.setData({
        starsOn,
        scoreText: rating.toFixed(1)
      })
    }
  }
})
