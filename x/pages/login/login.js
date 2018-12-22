const app = getApp()
const bcrypt = require('../../utils/miniprogram_npm/bcryptjs/index.js')

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
    wx.showLoading({
      title: 'loading...',
    })
    wx.request({
      url: app.globalData.url+'/api/salt',
      method: 'GET',
      data: {
        cellPhone: self.data.Id
      },
      success: res => {
        if(res.data.errMsg){
          wx.showToast({
            title: res.data.errMsg,
            icon: 'none'
          })
        }else{
          let hash = bcrypt.hashSync(self.data.password,res.data.salt)
          console.log(res.data.salt)
          console.log(hash)
          wx.request({
            url: app.globalData.url + '/api/pwlogin',
            method: 'POST',
            data: {
              openId: app.globalData.openId,
              cellPhone: self.data.Id,
              hash: hash
            },
            success: res => {
              if(res.data.errMsg){
                wx.showToast({
                  title: res.data.errMsg,
                  icon: 'none'
                })
              }else{
                wx.showToast({
                  title: '登录成功!',
                })
              }
            },
            fail: function () {
              wx.showToast({
                title: '登录失败!',
                icon: 'none'
              })
            }
          })
        }
      },
      fail: function () {
        wx.showToast({
          title: '连接失败!请检查网络',
          icon: 'none'
        })
      }
    })
  }
})


