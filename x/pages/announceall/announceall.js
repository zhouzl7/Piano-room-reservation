// pages/announceall/announceall.js
const app = getApp()
Page({


  /**
   * 页面的初始数据
   */
  data: {
    announce:[
      {
        title:"琴房一使用说明",
        time:"2018-11-21 21:40",
        author:"管理员",
        content:"lalala"
      },
      {
        title:"关于国庆放假琴房关闭说明",
        time:"2018-11-21 21:41",
        author:"author",
        content: "2-08，为键盘队专用琴房，键盘队自行，蒙楼负责登记管理；2-05，为键盘队与合唱队合用琴房，两队自行排队使用，蒙楼负责登记管理；2-01，为星海钢琴，为本校学生持学生琴卡使用，10元∕小时，应打2孔；2-02，2-03，2-04，2-06，2-07，向所有人开放，校内学生琴卡，15元∕小时，学生琴卡应打3孔∕小时；教职工卡，20元∕小时，教职工琴卡应打2孔∕小时；社会卡，30元∕小时，社会琴卡应打2孔∕小时；"
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
    let self = this
    wx.request({
      url: app.globalData.url + '/api/announcement',
      method: "GET",
      data: {
        openId: app.globalData.openId
      },
      success: res => {
        console.log(res.data)
        loadReservation(self, res.data.announce)
        console.log('Reservation loaded')
      },
      fail: function () {
        console.log('can\'t get reservation')
      }
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

  more_detail:function(event){
    var index = parseInt(event.currentTarget.dataset.index)
    wx.navigateTo({
      url: '../detail_announce/detail_announce?title=' + this.data.announce[index].title + '&time=' + this.data.announce[index].time + '&author=' + this.data.announce[index].author+'&content=' + this.data.announce[index].content,
    })
  }
  
})

function loadReservation(self, data) {
  console.log(data)
  self.setData({
    announce: data
  })
}