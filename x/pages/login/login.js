Page({
  /**
   * 初始化数据
   */
  data:{
    Id: '',
    password: '',
  },

  /**
   * 监听手机号输入
   */
  listenerIdInput: function(e) {
      this.data.Id = e.detail.value;

  },

  /**
   * 监听密码输入
   */
  listenerPasswordInput: function(e) {
      this.data.password = e.detail.value;
  },

  /**
   * 监听登录按钮
   */
  listenerLogin: function() {
      //打印收入账号和密码
    console.log('身份证号为: ', this.data.Id);
    console.log('密码为: ', this.data.password);
    if (this.data.Id.length == 0) 
    {
      wx.showToast
        ({
          title: '身份证号不能空',
          icon: 'loading',
          duration: 2000
        })
    }
    else if (this.data.password.length == 0)
    {
      wx.showToast
        ({
          title: '密码不能空',
          icon: 'loading',
          duration: 2000
        })
    }
    else {
      wx.showToast({
        title: '登录成功',
        icon: 'success',
        duration: 2000
      })
      
    }
  },
 

  onLoad:function(options){
    // 页面初始化 options为页面跳转所带来的参数
  },
  onReady:function(){
    // 页面渲染完成
  },
  onShow:function(){
    // 页面显示
  },
  onHide:function(){
    // 页面隐藏
  },
  onUnload:function(){
    // 页面关闭
  }
})

// Register a Page.
/*Page({

  onLoad: function () {
    const ctx = wx.createCanvasContext('myCanvas')
    //ctx.moveTo(0, 25)
    //ctx.lineTo(370, 25)
    //ctx.stroke()
    //ctx.draw()
  },
 
})*/

