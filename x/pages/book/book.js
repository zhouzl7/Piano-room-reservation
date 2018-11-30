// pages/book/book.js
const app = getApp()

Page({

    /**
     * 页面的初始数据
     */
    data: {
        time: [{
                id: 0,
                timestr: "8:00-9:00",
                color: "#fff"
            },
            {
                id: 1,
                timestr: "9:00-10:00",
                color: "#fff"
            },
            {
                id: 2,
                timestr: "10:00-11:00",
                color: "#fff"
            },
            {
              id: 3,
              timestr: "11:00-12:00",
              color: "#fff"
            },
            {
                id: 4,
                timestr: "12:00-13:00",
                color: "#fff"
            },
            {
                id: 5,
                timestr: "13:00-14:00",
                color: "#fff"
            },
            {
                id: 6,
                timestr: "14:00-15:00",
                color: "#fff"
            },
            {
              id: 7,
              timestr: "15:00-16:00",
              color: "#fff"
            },
            {
              id: 8,
              timestr: "16:00-17:00",
              color: "#fff"
            },
            {
              id: 9,
              timestr: "17:00-18:00",
              color: "#fff"
            },
            {
              id: 10,
              timestr: "18:00-19:00",
              color: "#fff"
            },
            {
              id: 11,
              timestr: "19:00-20:00",
              color: "#fff"
            },
            {
              id: 12,
              timestr: "20:00-21:00",
              color: "#fff"
            },
            {
              id: 13,
              timestr: "21:00-22:00",
              color: "#fff"
            },
        ],
        Days: [{
                name: "今天",
                room: [
                    {
                        name: "琴房1",
                        disabled: [false, false, false, false, false, false],
                        chosen: [false, true, false, false, false, false],
                        money: 15,
                        multiMoney: 30,
                        color: "#0090CE"
                    },
                    {
                        name: "琴房2",
                        disabled: [false, false, false, false, false, false],
                        chosen: [false, true, false, false, false, false],
                        money: 15,
                        multiMoney: 30,
                        color: "#fff"
                    }
                ],
                color: "#fff"
            },
            {
                name: "明天",
                room: [
                    {
                        name: "test",
                        disabled: [false, false, false, false, false, false],
                        chosen: [false, false, false, false, false, false],
                        money: 15,
                        multiMoney: 30,
                        color: "Yellow"
                    },
                    {
                        name: "wtf",
                        disabled: [false, false, false, false, false, false],
                        chosen: [false, false, false, false, false, false],
                        money: 15,
                        multiMoney: 30,
                        color: "#fff"
                    }
                ],
                color: "#fff"
            },
            {
                name: "后天",
                room: [
                    {
                        name: "wtf",
                        disabled: [false, false, false, false, false, false],
                        chosen: [false, false, false, false, false, false],
                        money: 15,
                        multiMoney: 30,
                        color: "#fff"
                    },
                    {
                        name: "test",
                        disabled: [false, false, false, false, false, false],
                        chosen: [false, false, false, false, false, false],
                        money: 15,
                        multiMoney: 30,
                        color: "#fff"
                    },
                    {
                        name: "test",
                        disabled: [false, false, false, false, false, false],
                        chosen: [false, false, false, false, false, false],
                        money: 15,
                        multiMoney: 30,
                        color: "#fff"
                    }
                ],
                color: "#fff"
            }
        ],
        chosenDay: 0,
        chosenRoom: 0,
        single: true,
        money: 0,
        singleMoney: 0,
        multiMoney: 0
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function() {
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
          console.log('success')
          load(self,res.data.Days)
          wx.showToast({
            title: 'BookLoaded!'
          })
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
            Days[0].color = "#0090CE"
            Days[0].room[0].color = "#0090CE"
            self.data.time.forEach(function (item) {
              item.color = "#fff"
            })
            self.setData({
              Days: Days,
              money: 0,
              multiMoney: 0,
              single: true,
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
     * 生命周期函数--监听页面显示
     */
    onShow: function() {
      /*
        const chosenDay = this.data.chosenDay
        const chosenRoom = this.data.chosenRoom
        const length = this.data.Days[chosenDay].room[chosenRoom].disabled.length
        this.data.Days[chosenDay].color = "#0090CE"
        this.data.Days[chosenDay].room[chosenRoom].color = "#0090CE"
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
            Days: this.data.Days
        })
        */
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
        this.data.Days[chosenDay].color = "#0090CE"
        if (this.data.Days[chosenDay].room.length <= chosenRoom) {
            chosenRoom = this.data.Days[chosenDay].room.length - 1
        }
        this.data.Days[chosenDay].room[chosenRoom].color = "#0090CE"
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
        this.data.Days[chosenDay].room[chosenRoom].color = "#0090CE"
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
        wx.showToast({
          title: this.data.time[index].timestr
        })
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

    singleChange: function(event) {
        if (event.detail.value) {
            this.setData({
                money: this.data.singleMoney,
                single: true
            })
        } else {
            this.setData({
                money: this.data.multiMoney,
                single: false
            })
        }
        console.log(this.data.single)
    },

    Book: function() {
      let self = this
      wx.showLoading({
        title: '预约中',
      })
      let booklist = []
      let bookTime = {
        day: 0,
        room: 0,
        time: 0
      }
      this.data.Days.forEach(function(item,index){
        bookTime.day = index
        item.room.forEach(function(item,index){
          bookTime.room = index
          item.chosen.forEach(function(item,index){
            if(item){
              bookTime.time = index
              booklist.push({
                day: bookTime.day,
                room: bookTime.room,
                time: index
              })
            }
          })
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
          if(res.statusCode === 200){
            console.log(res)
            bookChange(self,res.data.times)
            wx.showToast({
              title: '预约成功!',
            })
          }else if(res.statusCode === 403){
            console.log(res)
            bookChange(self, res.data.times)
            wx.showToast({
              title: '已有预约被占用!'
            })
          }
        },
        fail: function(){
          wx.showToast({
            title: '预约失败!',
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
  Days[0].color = "#0090CE"
  Days[0].room[0].color = "#0090CE"
  self.data.time.forEach(function (item) {
    item.color = "#fff"
  })
  self.setData({
    Days: Days,
    money: 0,
    singleMoney: 0,
    multiMoney: 0,
    single: true,
    chosenDay: 0,
    chosenRoom: 0,
    time: self.data.time
  })
}

function bookChange(self,data){
  //data:[{day,room,disabled}]
  console.log(data)
  data.forEach(item => {
    let param = {}
    param['Days[' + item.day + '].room[' + item.room + '].disabled'] = item.disabled
    param['Days[' + item.day + '].room[' + item.room +'].chosen'] = item.disabled.slice()
    param['Days[' + item.day + '].room[' + item.room + '].chosen'].fill(false)
    self.setData(param)
  })
}