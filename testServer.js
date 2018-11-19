console.log('test')

const Koa = require('koa');
const request = require('request');
const koaBody = require('koa-body');
//const http = require('http');
//const https = require('https');
//const fs = require('fs');
//const enforceHttps =  require('koa-sslify');

let Days = [{
    name: "今天",
    room: [
        {
            name: "琴房1",
            disabled: [true, true, false, false, false, false],
            money: 15,
            multiMoney: 30,
        },
        {
            name: "琴房2",
            disabled: [false, false, false, false, false, false],
            money: 15,
            multiMoney: 30,
        }
    ],
},
{
    name: "明天",
    room: [
        {
            name: "test",
            disabled: [false, false, false, false, false, false],
            money: 15,
            multiMoney: 30,
        },
        {
            name: "wtf",
            disabled: [false, false, false, false, false, false],
            money: 15,
            multiMoney: 30,
        }
    ],
},
{
    name: "后天",
    room: [
        {
            name: "wtf",
            disabled: [false, false, false, false, false, false],
            money: 15,
            multiMoney: 30,
        },
        {
            name: "test",
            disabled: [false, false, false, false, false, false],
            money: 15,
            multiMoney: 30,
        },
        {
            name: "test",
            disabled: [false, false, false, false, false, false],
            money: 15,
            multiMoney: 30,
        }
    ],
}
]

let reserve = [{
    room: "琴房1",
    useTime: "2018-11-17 13:00-14:00",
    user: "single",
    resTime: "xxxx-xx-xx xx:xx-xx:xx"
},
{
    room: "琴房2",
    useTime: "2018-11-18 13:00-14:00",
    user: "multy",
    resTime: "xxxx-xx-xx xx:xx-xx:xx"
}
]

let time = [
    {
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
]

let openId = '';


const app = new Koa();
app.use(koaBody({multipart: true}));
//app.use(enforceHttps());

app.listen(8888);

app.use(async (ctx,next) =>{
    if(ctx.request.path === '/api/login'){
        //console.log(ctx.request.query.code)
        let data = await reqUserInfo(ctx.request.query.code);
        let body = {};
        //console.log(data);
        if(data.openid){
        body.openId = data.openid;
        openId = data.openid;
        }
        else{
            body.openId = 'wtf';
        }
        //console.log(body)
        //let body = await getUserInfoFromDb(data);
        ctx.response.status = 200;
        ctx.response.body = body;
    }else{
        await next();
    }
});

app.use(async (ctx,next) =>{
    if(ctx.request.path === '/api/availableTime'){
        if(ctx.request.query.openId === openId){
            //console.log(Days)
            ctx.response.body = {
                Days: Days
            };
        }else{
            ctx.response.body = {
                Days: []
            };
        }
    }else{
        await next()
    }
})

app.use(async (ctx,next) => {
    if(ctx.request.path === '/api/reservation'){
        if(ctx.request.query.openId === openId){
            ctx.response.body = {
                reservation: reserve
            }
            ctx.response.code = 200
        }else{
            ctx.response.body = {
                reservation: reserve
            }
        }
    }else{
        await next()
    }
})

app.use(async (ctx,next) => {
    if(ctx.request.path === '/api/book'){
        //check if those have been booked.
        data = ctx.request.body.bookTime
        let canBook = true
        console.log(data)
        if(data){
            let newReserve = []
            data.forEach( item =>{
                console.log(item)
                if(Days[item.day].room[item.room].disabled[item.time] === false){
                    Days[item.day].room[item.room].disabled[item.time] = true
                    let param = {
                        room: Days[item.day].room[item.room].name,
                        useTime: Days[item.day].name + ' ' + time[item.time].timestr,
                        user: "single",
                        resTime: "????"
                    }
                    if(!ctx.request.body.single){
                        param.user = "multi"
                    }
                    newReserve.push(param)
                }else{
                    canBook = false
                }
            })
            if(canBook){
                ctx.response.statusCode = 200
                reserve = reserve.concat(newReserve)
            }else{
                ctx.response.statusCode = 403
            }
            let result = []
            let param = {}
            Days.forEach((item,index) =>{
                param.day = index
                item.room.forEach((item,index) =>{
                    result.push({
                        day: param.day,
                        room: index,
                        disabled: item.disabled
                    })
                })
            })
            ctx.response.body = {
                times: result
            }
        }else{
            let result = []
            let param = {}
            Days.forEach((item,index) =>{
                param.day = index
                item.room.forEach((item,index) =>{
                    param.room = index
                    param.disabled = item.disabled
                    result.push(param)
                })
            })
            ctx.response.body = {
                times: result
            }
        }
    }else{
        await next()
    }
})

//http.createServer(app.callback()).listen(80);
//https.createServer(options, app.callback()).listen(443);

function reqUserInfo(code){
    return new Promise(function (resolve,reject){
        request.get({
            url: 'https://api.weixin.qq.com/sns/jscode2session',
            json: true,
            qs: {
		        appid: 'wx77fa9e3e4014ff7a',
		        secret: '79e90ba6f0b6cab8b273cafd79fe1ba2',
                js_code: code,
                grant_type: 'authorization_code'
            }
        },function(err,res,data){
            if(res.statusCode === 200){
                openId = data.openId
                resolve(data);
            }else{
                resolve({
                    openId: 'wtf'
                });
            }
        });
    });
}

