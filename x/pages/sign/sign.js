const app = getApp()
const bcrypt = require('../../utils/miniprogram_npm/bcryptjs/index.js')
Page({

  /**
   * 初始化数据
   */
  data: {
    Id: '',
    name:'',
    password: '',
    password2:'',
    displayIdErr: 'none',
    displayNameErr: 'none',
    displayPwErr: 'none',
    displayPwConfirmErr: 'none'
  },

  /**
   * 监听身份证号输入
   */
  listenerIdInput: function (e) {
    this.setData({
      displayIdErr: 'none'
    })
    this.data.Id = e.detail.value
  },
  /**
   * 监听密码输入
   */
  listenerPasswordInput: function (e) {
    this.data.password = e.detail.value
    this.setData({
      displayPwErr: 'none'
    })
  },
  listenerPassword2Input: function (e) {
    this.data.password2 = e.detail.value
    this.setData({
      displayPwConfirmErr: 'none'
    })
  },
  /**
 * 监听姓名输入
 */
  listenerNameInput: function (e) {
    this.data.name = e.detail.value
    this.setData({
      displayNameErr: 'none'
    })
  },
  /**
   * 监听登录按钮
   */
  listenerLogin: function () {
    let invalidInput = false
    if(!this.data.Id){
      //TODO: 
      this.setData({
        displayIdErr: 'inline'
      })
      invalidInput = true
    }
    if(!this.data.name){
      //TODO: Label 姓名不能为空
      this.setData({
        displayNameErr: 'inline'
      })
      invalidInput = true
    }
    if(this.data.password.length <= 8){
      //TODO: 密码长度过小
      this.setData({
        displayPwErr: 'inline'
      })
      invalidInput = true
    }
    if(this.data.password !== this.data.password2){ 
      //TODO: Label 两次输入密码不一致
      this.setData({
        displayPwConfirmErr: 'inline'
      })
      invalidInput = true
    }
    if(invalidInput){
      return
    }
    console.log('validInput')
    let self = this
    wx.request({
      url: app.globalData.url+'/api/salt',
      method: "GET",
      success: res => {
        if(res.data.errMsg){
          wx.showToast({
            title: res.data.errMsg,
            icon: "none"
          })
        }else {
          //create hash with salt.
          let hash = bcrypt.hashSync(self.data.password,res.data.salt)
          wx.request({
            url: app.globalData.url+'/api/register',
            method: "POST",
            data:{
              openId: app.globalData.openId,
              name: self.data.name,
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
                  title: '注册成功!',
                })
                wx.switchTab({
                  url: '../home/home',
                })
                console.log('1')
              }
            },
            fail: function () {
              wx.showToast({
                title: '注册失败!请稍后重试',
                icon: 'none'
              })
            }
          })
        }
      },
      fail: function () {
        wx.showToast({
          title: '连接失败, 请检查您的网络状态',
          icon: 'none'
        })
      }
    })
  },

  onLoad: function (options) {
    // 页面初始化 options为页面跳转所带来的参数
  },
  onReady: function () {
    // 页面渲染完成
  },
  onShow: function () {
    // 页面显示
  },
  onHide: function () {
    // 页面隐藏
  },
  onUnload: function () {
    // 页面关闭
  }
})

