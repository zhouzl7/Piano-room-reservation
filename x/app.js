//app.js
App({
  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    var self = this
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        console.log(res.code)
        if(res.code){
          wx.request({
            url: self.globalData.url + "/api/login",
            data: {
              code: res.code
            },
            method: 'GET',
            success: res => {
              console.log('loginSucceed');
              self.globalData.openId = res.data.openId
              console.log(self.globalData)
            },
            fail: function () {
              console.log('res.code.fail')
              wx.navigateTo({
                url: './pages/login/login',
              })
            }
          })

        }
      },
    })
    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              this.globalData.userInfo = res.userInfo

              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  },
  globalData: {
    userInfo: null,
    url: "https://166628.iterator-traits.com",
    //url:"https://localhost",
    openId: null
  }
})