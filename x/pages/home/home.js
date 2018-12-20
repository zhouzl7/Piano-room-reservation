// pages/hometest/home test.js
//const crypt = require('../../utils/miniprogram_npm/pbkdf2/index.js')


const app = getApp()
Page({
  data: {
    color: "darkgrey",
    allroom:[
      {
        room_type:"星海琴房",
        room:"101 202" 
      },
      {
        room_type: "大琴房",
        room: "303"
      },
      {
        room_type: "小琴房",
        room: "404"
      }
    ]
  },
  onShow: function () {
    let self = this
    wx.request({
      url: app.globalData.url + '/api/room',
      method: "GET",
      data: {
        openId: app.globalData.openId
      },
      success: res => {
        console.log(res.data)
        loadRoom(self, res.data.allroom)
        console.log('Room loaded')
      },
      fail: function () {
        console.log('can\'t get room')
      }
    })
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
    if (this.data.color === "cornflowerblue") {
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

function loadRoom(self, data) {
  console.log(data)
  self.setData({
    allroom: data
  })
}