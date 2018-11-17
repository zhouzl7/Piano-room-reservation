// pages/book/book.js
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
                timestr: "13:00-14:00",
                color: "#fff"
            },
            {
                id: 4,
                timestr: "14:00-15:00",
                color: "#fff"
            },
            {
                id: 5,
                timestr: "15:00-16:00",
                color: "#fff"
            }
        ],
        Days: [{
                id: "今天",
                room: [{
                        name: "琴房1",
                        disabled: [true, true, false, false, false, false],
                        chosen: [false, false, false, false, false, false],
                        money: 15,
                        multiMoney: 30,
                        color: "#fff"
                    },
                    {
                        name: "琴房2",
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
                id: "明天",
                room: [{
                        name: "test",
                        disabled: [false, false, false, false, false, false],
                        chosen: [false, false, false, false, false, false],
                        money: 15,
                        multiMoney: 30,
                        color: "#fff"
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
                id: "后天",
                room: [{
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
    onLoad: function() {},

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function() {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function() {
        //TODO: 刷新当前可用时间.
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
            //this.data.money = this.data.singleMoney
        this.setData({
            time: this.data.time,
            Days: this.data.Days,
            money: this.data.money,
            singleMoney: this.data.singleMoney,
            multiMoney: this.data.multiMoney
        })
    },

    singleChange: function(event) {
        console.log(event)
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
    }
})