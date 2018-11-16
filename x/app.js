App({//如下为小程序的生命周期
  onLaunch: function () { },//监听初始化
  onShow: function () { },//监听显示（进入前台）
  onHide: function () { },//监听隐藏（进入后台：按home离开微信）
  onError: function (msg) { },//监听错误
  //如下为自定义的全局方法和全局变量  
  globalFun: function () { },
  globalData: 'I am global data'
})