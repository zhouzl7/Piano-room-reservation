// pages/book/book.js
const app = getApp()

Page({

    /**
     * 页面的初始数据
     */
    data: {
        time: [],
        Days: [],
        chosenDay: 0,
        chosenRoom: 0,
        single: true,
        money: 0,
        singleMoney: 0,
        multiMoney: 0,
        fontcolor: "darkgrey",
        singleopacity: 0.5,
        multiopacity: 0.5,
        bind: false
    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function() {
      let time = []
      for(let i = 0;i < 14;i++){
        time.push({
          id: i,
          timestr: (i+8) + ':00-' + (i+9) + ':00',
          color: '#fff'
        })
      }
      this.setData({
        time: time
      })
      let self = this
      wx.showLoading({
        title: 'loading...',
      })
      wx.request({
        url: app.globalData.url + '/api/availableTime',
        data: {
          openId: app.globalData.openId
        },
        method: "GET",
        success: res => {
          if(res.data.errMsg){
            wx.showToast({
              title: res.data.errMsg,
              icon: 'none'
            })
            self.setData({
              bind: false
            })
          }else{
            load(self, res.data.Days)
            wx.showToast({
              title: 'BookLoaded!'
            })
          }
        },
        fail: function () {
          setTimeout(function () {
            let Days = self.data.Days
            Days.forEach(function (item, index) {
              item.color = "#fff"
              item.room.forEach(function (item, index) {
                item.chosen = item.disabled.slice()
                item.chosen.fill(false)
                item.color = "#fff"
              })
            })
            Days[0].color = "cornflowerblue"
            Days[0].room[0].color = "cornflowerblue"
            self.data.time.forEach(function (item) {
              item.color = "#fff"
            })
            self.setData({
              Days: Days,
              money: 0,
              multiMoney: 0,
              single: true,
              singleopacity: 1,
              chosenDay: 0,
              chosenRoom: 0,
              time: self.data.time
            })
          }, 0)
          wx.showToast({
            title: 'loginFailed!',
            icon: 'none'
          })
        }
      })
    },

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function() {

    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function() {

    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function() {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function() {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function() {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function() {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function() {

    },

    chooseDay: function(event) {
        let chosenDay = this.data.chosenDay
        let chosenRoom = this.data.chosenRoom
        let length = this.data.Days[chosenDay].room[chosenRoom].disabled.length
        this.data.Days[chosenDay].color = "#fff"
        this.data.Days[chosenDay].room[chosenRoom].color = "#fff"
        chosenDay = event.currentTarget.dataset.id
        this.data.Days[chosenDay].color = "cornflowerblue"
        if (this.data.Days[chosenDay].room.length <= chosenRoom) {
            chosenRoom = this.data.Days[chosenDay].room.length - 1
        }
        this.data.Days[chosenDay].room[chosenRoom].color = "cornflowerblue"
        for (let i = 0; i < length; i++) {
            if (this.data.Days[chosenDay].room[chosenRoom].disabled[i]) {
                this.data.time[i].color = "#fff"
            } else {
                if (this.data.Days[chosenDay].room[chosenRoom].chosen[i]) {
                    this.data.time[i].color = "Yellow"
                } else {
                    this.data.time[i].color = "#fff"
                }
            }
        }
        this.setData({
            time: this.data.time,
            Days: this.data.Days,
            chosenDay: chosenDay,
            chosenRoom: chosenRoom
        })
    },

    chooseRoom: function(event) {
        let chosenDay = this.data.chosenDay
        let chosenRoom = this.data.chosenRoom
        let length = this.data.Days[chosenDay].room[chosenRoom].disabled.length
        this.data.Days[chosenDay].room[chosenRoom].color = "#fff"
        chosenRoom = event.currentTarget.dataset.id
        this.data.Days[chosenDay].room[chosenRoom].color = "cornflowerblue"
        for (let i = 0; i < length; i++) {
            if (this.data.Days[chosenDay].room[chosenRoom].disabled[i]) {
                this.data.time[i].color = "#fff"
            } else {
                if (this.data.Days[chosenDay].room[chosenRoom].chosen[i]) {
                    this.data.time[i].color = "Yellow"
                } else {
                    this.data.time[i].color = "#fff"
                }
            }
        }
        this.setData({
            time: this.data.time,
            Days: this.data.Days,
            chosenRoom: chosenRoom
        })
    },

    chooseTime: function(event) {
        let index = event.currentTarget.dataset.id
        let chosenDay = this.data.chosenDay
        let chosenRoom = this.data.chosenRoom
        if (this.data.Days[chosenDay].room[chosenRoom].chosen[index] === false) {
            //改变chosen, 增加money, 变色
            this.data.time[index].color = "yellow"
            this.data.Days[chosenDay].room[chosenRoom].chosen[index] = true
            this.data.singleMoney += this.data.Days[chosenDay].room[chosenRoom].money
            this.data.multiMoney += this.data.Days[chosenDay].room[chosenRoom].multiMoney
        } else {
            this.data.time[index].color = "#fff"
            this.data.Days[chosenDay].room[chosenRoom].chosen[index] = false
            this.data.singleMoney -= this.data.Days[chosenDay].room[chosenRoom].money
            this.data.multiMoney -= this.data.Days[chosenDay].room[chosenRoom].multiMoney
        }
        this.data.money = this.data.single ? this.data.singleMoney : this.data.multiMoney
        this.setData({
            time: this.data.time,
            Days: this.data.Days,
            money: this.data.money,
            singleMoney: this.data.singleMoney,
            multiMoney: this.data.multiMoney
        })
    },

    chooseSingle: function () {
        this.setData({
          money: this.data.singleMoney,
          single: true,
          singleopacity: 1,
          multiopacity: 0.5
        })
    },

    chooseMulti: function () {
      this.setData({
        money: this.data.multiMoney,
        single: false,
        singleopacity: 0.5,
        multiopacity: 1
      })
    },

    Book: function() {
      let self = this
      wx.showLoading({
        title: '预约中',
      })
      let booklist = []
      let bookTime = {
      }
      this.data.Days.forEach(function(item,index){
        bookTime.day = index
        item.room.forEach(function(item,index){
          bookTime.room = item.name
          bookTime.time = []
          item.chosen.forEach(function(item,index){
            if(item){
              bookTime.time.push('Time'+(index+1))
            }
          })
          if(bookTime.time.length > 0){
            booklist.push({
              day: bookTime.day,
              room: bookTime.room,
              time: bookTime.time
            })
          }
        })
      })
      wx.request({
        url: app.globalData.url+'/api/book',
        method: 'POST',
        data:{
          bookTime: booklist,
          single: self.data.single,
          openId: app.globalData.openId
        },
        success: res => {
          console.log(res)
          if(res.data.times){
            bookChange(self,res.data.times)
          }
          if(res.data.errMsg){
            wx.showToast({
              title: res.data.errMsg,
              icon: 'none'
            })
          }else{
            wx.showToast({
              title:'预约成功!'
            })
          }
        },
        fail: function(){
          wx.showToast({
            title: '请求超时!',
            icon: 'none'
          })
        },
        complete: function(){
          self.data.time.forEach(item =>{
            item.color = "#fff"
          })
          self.data.Days.forEach(item => {
            item.room.forEach(item => {
              item.chosen.fill(false)
            })
          })
          self.setData({
            Days: self.data.Days,
            time: self.data.time,
            money: 0,
            singleMoney: 0,
            multiMoney: 0,
            single: true
          })
        }
      })
    }
})

function load(self,data){
  let Days = data
  console.log(Days)
  Days.forEach(function (item, index) {
    item.color = "#fff"
    item.room.forEach(function (item, index) {
      item.chosen = item.disabled.slice()
      item.chosen.fill(false)
      item.color = "#fff"
    })
  })
  Days[0].color = "cornflowerblue"
  Days[0].room[0].color = "cornflowerblue"
  self.data.time.forEach(function (item) {
    item.color = "#fff"
  })
  self.setData({
    Days: Days,
    money: 0,
    singleMoney: 0,
    multiMoney: 0,
    single: true,
    singleopacity: 1,
    multiopacity: 0.5,
    chosenDay: 0,
    chosenRoom: 0,
    bind: true,
    time: self.data.time
  })
}

function bookChange(self,data){
  //data:[{day,room,disabled}]
  console.log(data)
  data.forEach(item => {
    let roomName = item.room
    let roomIndex = -1
    self.data.Days[item.day].room.forEach((item,index)=>{
      if(item.name === roomName){
        roomIndex = index
        return
      }
    })
    if(roomIndex === -1){
      return
    }
    let param = {}
    param['Days[' + item.day + '].room[' + roomIndex + '].disabled'] = item.disabled
    param['Days[' + item.day + '].room[' + roomIndex +'].chosen'] = item.disabled.slice()
    param['Days[' + item.day + '].room[' + roomIndex + '].chosen'].fill(false)
    console.log(param)
    self.setData(param)
  })
}