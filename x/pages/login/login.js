Page({
  /**
   * 初始化数据
   */
  data: {
    Id: '',
    password: '',
  },

  /**
   * 监听手机号输入
   */
  listenerIdInput: function (e) {
    this.data.Id = e.detail.value;

  },

  /**
   * 监听密码输入
   */
  listenerPasswordInput: function (e) {
    this.data.password = e.detail.value;
  },

  /**
   * 监听登录按钮
   */



  onLoad: function (options) {
    // 页面初始化 options为页面跳转所带来的参数
  },
  onReady: function () {
    // 页面渲染完成
  },
  onShow: function () {
  },
  onHide: function () {
    // 页面隐藏
  },
  onUnload: function () {
    // 页面关闭
  },
  listenerLogin: function () {
    let self = this
    wx.request({
      url: app.globalData.url + '/api/outlogin',
      method: 'POST',
      data: {
        openId: app.globalData.openId
      },
      success: res => {
        if (res.statusCode === 200) {
          console.log(res)
          wx.showToast({
            title: '登录成功!',
            icon: 'success'
          })
        } else if (res.statusCode === 403) {
          console.log(res)
          wx.showToast({
            title: '不能输入空',
            icon: 'loading'
          })
        }
      },
      fail: function () {
        wx.showToast({
          title: '登录失败!',
          icon: 'none'
        })
      },
      complete: function () {
        self.setData({
          Id: self.data.Id,
          password: self.data.password
        })
      }
    })
  }
})
function OutIdLogin(self, data) {
  console.log(data)
}


