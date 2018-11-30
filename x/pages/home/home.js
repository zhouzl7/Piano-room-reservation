// pages/hometest/home test.js
Page({
  data: {
    color: "darkgrey",
  },
  change: function (event) {
    wx.navigateTo({
      url: '../announceall/announceall',
    })
  },
  toNotice: function (event) {
    this.setData({
      color: "cornflowerblue"
    })
    wx.navigateTo({
      url: '../notice/notice',
    })
  },
  changecolor: function (event) {
    if (this.data.color == "cornflowerblue") {
      this.setData({
        color: "darkgrey"
      })
    } else {
      this.setData({
        color: "cornflowerblue"
      })
    }
  }
})