// pages/alreadyBind/alreadyBind.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    name: null,
    personId: null,
    userGroup: null,
    xinghaiPrice: null,
    smallPrice: null,
    bigPrice: null,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    wx.request({
      url: app.globalData.url + '/api/isBind',
      data: {
        openId: app.globalData.openId
      },
      method: "GET",
      success: res => {
        console.log(res)
        if (res.data.errMsg) { }
        else {
          this.setData({
            name: res.data.name,
            personId: res.data.personId,
            userGroup: res.data.userGroup,
            xinghaiPrice: res.data.xinghaiPrice,
            smallPrice: res.data.smallPrice,
            bigPrice: res.data.bigPrice,
          })
        }
      },
    })
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  notBind: function (event) {
    wx.request({
      url: app.globalData.url + '/api/notBind',
      data: {
        openId: app.globalData.openId
      },
      method: "GET",
      success: res => {
        console.log(res)
        if (res.data.errMsg) {
          wx.showToast({
            title: '未绑定',
          })
        }
        else {
          wx.showToast({
            title: '解绑成功',
          })
          wx.switchTab({
            url: '../home/home',
          })
        }
      },
    })
  }
})