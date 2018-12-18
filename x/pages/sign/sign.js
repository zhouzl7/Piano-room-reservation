Page({

  /**
   * 初始化数据
   */
  data: {
    Id: '',
    name:'',
    password: '',
    password2:'',
  },

  /**
   * 监听身份证号输入
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
  listenerPassword2Input: function (e) {
    this.data.password2 = e.detail.value;
  },
  /**
 * 监听姓名输入
 */
  listenerNameInput: function (e) {
    this.data.name = e.detail.value;
  },
  /**
   * 监听登录按钮
   */
  listenerLogin: function () {
    //打印收入账号和密码
    console.log('身份证号为: ', this.data.Id);
    console.log('姓名为: ', this.data.name);
    console.log('密码为: ', this.data.password);
    console.log('确认密码为: ', this.data.password2);
    if(this.data.password==this.data.password2)
    { 
      wx.navigateTo({
        url: '../login/login',
      })
      console.log("success");}
    else
    { console.log("fail");}
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