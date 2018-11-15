//firstpage.js
//首页

Page({
  change:function(event){
    wx.redirectTo({
      url: '../index/index',
      success: function (res) {
        // success
        console.log(成功);
      },
      fail: function () {
        // fail
        console.log('sksdfksjfksjf');
      },
    })
  }
})
