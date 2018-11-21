//firstpage.js
//首页

Page({
    data: {
        color: "#fff",
    },
    change: function(event) {
        wx.navigateTo({
            url: '../announceall/announceall',
        })
    },
    toNotice: function(event) {
        wx.navigateTo({
            url: '../notice/notice',
        })
    },
    changecolor: function(event) {
        if (this.data.color == "yellow") {
            this.setData({
                color: "#fff"
            })
        } else {
            this.setData({
                color: "yellow"
            })
        }
    }
})