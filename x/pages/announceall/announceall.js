// pages/announceall/announceall.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    announce:[
      {
        title:"琴房一使用说明",
        time:"2018-11-21 21:40"
      },
      {
        title:"关于国庆放假琴房关闭说明",
        time:"2018-11-21 21:41"
      }
    ]
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

  more_detail:function(event){
    wx.navigateTo({
      url: '../detail_announce/detail_announce',
    })
  }
})