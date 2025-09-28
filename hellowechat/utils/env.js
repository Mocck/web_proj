const { USE_MOCK_DEFAULT } = require('../config/index')
const KEY = 'USE_MOCK_OVERRIDE'
function getUseMock() {
  const v = wx.getStorageSync(KEY)
  return (v === '' || v === undefined || v === null) ? USE_MOCK_DEFAULT : !!v
}
function setUseMock(v) { wx.setStorageSync(KEY, !!v) }
module.exports = { getUseMock, setUseMock }
