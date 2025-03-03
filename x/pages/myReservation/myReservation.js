// pages/myReservation/myReservation.js
const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        colorUnuse: "#0090CE",
        colorHistory: "#fff",
      reserve: [{
        room: "琴房1",
        status: "已赴约",
        people: "测试员1号",
        useTime: "2018-11-17 13:00-14:00",
        is_pay: "已付款",
        user: "single",
        resTime: "xxxx-xx-xx xx:xx-xx:xx"
      },
      {
        room: "琴房2",
        status: "已赴约",
        people: "测试员1号",
        useTime: "2018-11-18 13:00-14:00",
        is_pay: "已付款",
        user: "multy",
        resTime: "xxxx-xx-xx xx:xx-xx:xx"
      }
      ]
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function(options) {

    },

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function() {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function() {
      //刷新预约情况
      let self = this
      wx.request({
        url: app.globalData.url + '/api/reservation',
        method: "GET",
        data: {
          openId: app.globalData.openId
        },
        success: res => {
          console.log(res.data)
          loadReservation(self,res.data.reserve)
          console.log('Reservation loaded')
        },
        fail: function(){
          console.log('can\'t get reservation')
        }
      })
    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function() {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function() {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function() {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function() {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function() {

    },

})

function loadReservation(self,data){
  console.log(data)
  self.setData({
    reserve: data
  })
}