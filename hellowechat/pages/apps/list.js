const { getApps } = require('../../data/getApps')
const { getUseMock, setUseMock } = require('../../utils/env')

Page({
  data: {
    useMock: getUseMock(),
    list: [],
    loading: false,
    error: '',
    skeleton: new Array(6).fill(0)
  },

  onLoad() { this.loadData() },

  onPullDownRefresh() {
    this.loadData().finally(() => wx.stopPullDownRefresh())
  },

  onToggleMock(e) {
    const v = !!e.detail.value
    setUseMock(v)
    this.setData({ useMock: v })
    this.loadData()
  },

  async loadData() {
    this.setData({ loading: true, error: '' })
    try {
      const list = await getApps()
      this.setData({ list })
    } catch (e) {
      this.setData({ error: e.message || '加载失败' })
    } finally {
      this.setData({ loading: false })
    }
  }
})
