from flask import request, Flask, jsonify
import hashlib
import sql
import random
import codemao
import requests
import re


html = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="Mark Otto, Jacob Thornton, and Bootstrap contributors">
    <meta name="generator" content="Jekyll v4.0.1">
    <title>编程猫账号登录|学猫叫</title>

    <link rel="canonical" href="https://getbootstrap.com/docs/4.5/examples/sign-in/">

    <!-- Bootstrap core CSS -->
<link href="/static/assets/dist/css/bootstrap.css" rel="stylesheet">

    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }
    </style>
    <!-- Custom styles for this template -->
    <link href="/static/signin.css" rel="stylesheet">
  </head>
  <body class="text-center">

    
  <div class="form-signin" id="form">
  <img class="mb-4" src="https://getbootstrap.net/example/assets/brand/bootstrap-solid.svg" alt="" width="72" height="72">
  <h1 class="h3 mb-3 font-weight-normal">请登录您的编程猫账号</h1>

  <label for="inputID" class="sr-only">编程猫账号</label>
  <input type="text" onkeydown=show() id="userid" class="form-control" placeholder="编程猫账号" required autofocus>

  <label for="inputPassword" class="sr-only">Password</label>
  <input type="password" onkeydown=show() id="userpassword" class="form-control" placeholder="编程猫密码" required>
  
  <button class="btn btn-lg btn-primary btn-block" id='Ender' onclick=login()>登录</button>
  <p class="mt-5 mb-3 text-muted">&copy; 2017-2020</p>
  </div>

<script>
  function success(data){
    alert(data.message);
    document.getElementById("Ender").removeAttribute("disabled");
    if (data.message == '登录成功，准备跳转'){
      var gotourl = data.return
      window.location.href=gotourl;
    }
  }

  function login(){
  document.getElementById("Ender").setAttribute("disabled", true);
  var id = document.getElementById("userid").value
  var passwd = document.getElementById("userpassword").value
  var pagesurl = window.location.href;
  var posturl = pagesurl.replace('/login/', '/post/')
  var data = {"phone":id,"password":passwd}
  if (id == ''){
      alert('账号不可为空')
      document.getElementById("Ender").removeAttribute("disabled");
      return ;
  }
  if (passwd == ''){
      alert('密码不可为空')
      document.getElementById("Ender").removeAttribute("disabled");
      return ;
  }

  var httpRequest = new XMLHttpRequest();//第一步：创建需要的对象
  httpRequest.open('POST', posturl, true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
  httpRequest.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）var obj = { name: 'zhansgan', age: 18 };
  httpRequest.send(JSON.stringify(data));//发送请求 将json写入send中

  httpRequest.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
    if (httpRequest.readyState == 4 && httpRequest.status == 200) {//验证请求是否发送成功
        var json = httpRequest.responseText;//获取到服务端返回的数据
        var obj = JSON.parse(json);
        success(obj);
    }
};

  }

function show(){
      var e=window.event||arguments.callee.caller.arguments[0];
      if(e.keyCode==13){
          login()
      }
    }
   
</script>
</body>
</html>

'''

app=Flask(__name__) 

@app.route('/newloginrequest',methods=['POST'])     
def newloginre():   

    try:
        data =  request.form
        inputad = str(data['AD']) 
        inputsalt = str(data['salt'])
        inputkey = str(data['key'])
        inputcallback = str(data['callback'])
        inputreturn = str(data['return'])
    except KeyError:
        return {"code":"Error","message":"缺失参数！"}
    
    userlist = sql.queries('SELECT * FROM user;')

    if inputad in str(userlist):
        for i in range(len(userlist)):
            if userlist[i][0] == inputad:
                trueak = userlist[i][1]
                break
    else:
        return {"code":"Error","message":"无效的AD！"}

    daimd5 = inputad+trueak+inputsalt+inputcallback+inputreturn
    truesign = hashlib.md5(daimd5.encode('utf-8')).hexdigest()

    if truesign == inputkey:
        loginid = random.randint(100000000,999999999)
        sql.write(f'INSERT INTO loginre VALUES ({loginid},"peting","{inputcallback}","{inputreturn}");')
        return {
            "code":"OK",
            "AD":inputad,
            "loginurl":'https://api.syrathon.com/codemaologin/login/' + str(loginid),
            "callbackurl":inputcallback,
            "loginid":str(loginid)


        }
    else:
        return {"code":"Error","message":"签名错误！"}

@app.route('/codemaologin/login/<loginid>',methods=['GET'])
def login(loginid):
    loginlog = sql.queries(f'SELECT * FROM loginre WHERE type="peting" AND loginid = {loginid}')
    if loginid in str(loginlog):
        return html
    else:
        return "没有这个登录请求"

@app.route('/codemaologin/post/<loginid>',methods=['POST'])
def postlogin(loginid):
    loginlog = sql.queries(f'SELECT * FROM loginre WHERE type="peting" AND loginid = {loginid}')
    if loginid in str(loginlog):
        data =  request.get_json()
        try:
            phone = str(data['phone'])
            password = str(data['password'])
        except KeyError:
            return {"code":"ERROR","message":"缺失参数"}
        data = sql.queries(f'SELECT * FROM loginre WHERE loginid={loginid} AND type="peting"')
        callback = data[0][2]
        returnurl = data[0][3]
        back = codemao.codemao(phone, password)
        if 'ERROR' in str(back):
            return({"code":"ERROR","message":"用户名或密码错误"})
        else:
            try:
                back.update(loginid=loginid)
                HTTPPOST = requests.post(callback,data=back)
            except OSError:
                print(callback)
                return {"code":"ERROR","message":"未能通知回调地址"}
            else:
                if 'OK' == HTTPPOST.text:
                    return({"code":"OK","message":"登录成功，准备跳转","return":returnurl})
                else:
                    print(callback)
                    return {"code":"ERROR","message":"未能通知回调地址"}
                    
    else:
            return {"code":"ERROR","message":"无效的登录请求"}
    
@app.route('/test',methods=['POST'])
def test():
    data =  request.form
    print(data)
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True,port=80)              #启动这个应用服务器，并开启debug,才能定位问题