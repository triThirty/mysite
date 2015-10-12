$(document).ready(function(){
    var ws = new WebSocket("ws://localhost:8080/testChatroom");
    showOnLineUsers();
    showChoice();
    changeRoomName();
    alert(document.cookie);
    ws.onmessage = function(event){
        var js = event.data;
        var data = JSON.parse(js)
        
        if(data.type=="sys-online"){  
            var talk_div = document.createElement("div");
            talk_div.className="talk system";
            talk_div.innerHTML="►► "+data.info.nick_name+" 加入房间";
            $("#talks").prepend(talk_div);
        }
        else if(data.type=="user"){
            var dl_talk = showTalks(data,getTailWrep());
            $("#talks").prepend(dl_talk);
        }
        else if(data.type=="sys-offline"){
            var talk_div = document.createElement("div");
            talk_div.className="talk system";
            talk_div.innerHTML="►► "+data.info.nick_name+" 退出房间";
            $("#talks").prepend(talk_div);
        }
    }
    
   $("#room-submit-btn").click(function(){ 
       var text = $("#message-textarea").val();
       if(text!=""&&text.length<=140){
        ws.send($("#message-textarea").val());
       }
       else{
           alert("输入内容过长（140字内）或为空");
       }
   })
});

//隐藏登出窗体
$(document).mousedown(
 function(event){
     if(event.target.className.indexOf("dropdown-menu")<0){
            $("#talkSetting").css("opacity","0.4");
            $("#talkSetting").removeClass("open");
            $(".preferences").attr("aria-expanded","false");
     }
  }
);

//构造展示聊天记录模块
function showTalks(data,tail){
    var talk_dl = document.createElement("dl");
       
    var talk_dl_dt = document.createElement("dt");
    var talk_dl_div1 = document.createElement("div");
    var talk_dl_div2 = document.createElement("div");
    var talk_dl_div1_span = document.createElement("span");
    var talk_dl_div2_span = document.createElement("span");
    talk_dl.className="talk "+data.info.avatar;
    talk_dl_dt.className="dropdown";
    talk_dl_div1.className="avatar avatar-"+data.info.avatar;
    talk_dl_div2.className="name";
    talk_dl_div2.setAttribute("data-toggle","dropdown");
    talk_dl_div1_span.innerHTML=data.info.nick_name;
    talk_dl_div2_span.className="select-text";
    talk_dl_div2_span.innerHTML=data.info.nick_name;
    
    talk_dl_div1.appendChild(talk_dl_div1_span);
    talk_dl_div2.appendChild(talk_dl_div2_span);
    talk_dl_dt.appendChild(talk_dl_div1);
    talk_dl_dt.appendChild(talk_dl_div2);
    talk_dl.appendChild(talk_dl_dt);
    
    var talk_dl_dd = document.createElement("dd");
    var talk_dl_dd_div1 = document.createElement("div");
    var talk_dl_dd_div2 = document.createElement("div");
    var talk_dl_dd_div3 = document.createElement("div");   
    var talk_dl_dd_p = document.createElement("p");  
    
    talk_dl_dd.className="bounce";
    talk_dl_dd_div1.className="bubble";
    talk_dl_dd_div2.className="tail-wrap "+getTailWrep();
    talk_dl_dd_div2.style="background-size: 65px;";
    talk_dl_dd_div3.className="tail-mask";
    talk_dl_dd_p.className="body select-text";
    talk_dl_dd_p.innerHTML=data.info.msg;
    
    talk_dl_dd_div2.appendChild(talk_dl_dd_div3);
    talk_dl_dd_div1.appendChild(talk_dl_dd_div2);
    talk_dl_dd_div1.appendChild(talk_dl_dd_p);
    talk_dl_dd.appendChild(talk_dl_dd_div1);
    talk_dl.appendChild(talk_dl_dd);
    
    return talk_dl;
   }
//显示在线人员
function showOnLineUsers(){
    $("#onlineUser").click(
    function(){   
            $("#members").animate({height:"toggle"});
        }  
    );
}
//显示登出窗体
function showChoice(){
    $("#talkSetting").click(
        function(){            
            $("#talkSetting").css("opacity","1");
            $("#talkSetting").addClass("open");
            $(".preferences").attr("aria-expanded","true");
        }
    );
}

//构造聊天框小尾巴
function getTailWrep(){
        var now =new Date();
        var number =now.getSeconds()%3;
        if(number==0){
            return "top";
        }
        else if(number==1){
            return "center";
        }
        else if(number==2){
            return "bottom";
        }
    }

//改变聊天室名称
function changeRoomName(){
    var roomName=$(".room-title-name").html();
    
    var span_div = document.createElement("div");
    var name_input=document.createElement("input");
    var bun_span=document.createElement("span");
    var bun1=document.createElement("button");
    var bun2=document.createElement("button");
    span_div.className="input-group input-group-sm";
    span_div.setAttribute("id","room-name-input");
    name_input.className="form-control form-inline";
    name_input.setAttribute("placeholder","Room name");
    name_input.setAttribute("type","text");
    name_input.setAttribute("name","room_name");
    name_input.setAttribute("maxlength","20");
    name_input.setAttribute("style","position: inline-block");
    name_input.setAttribute("value",roomName);
    
    bun_span.className="input-group-btn";
    bun1.className="btn btn-primary";
    bun1.setAttribute("type","submit");
    
    bun1.setAttribute("disabled","true");
    bun1.innerHTML="修改";
    bun2.className="btn btn-default";
    bun2.setAttribute("type","button");
    bun2.innerHTML="取消";
    
    bun_span.appendChild(bun1);
    bun_span.appendChild(bun2);
    
    span_div.appendChild(name_input);
    span_div.appendChild(bun_span);

    $(".room-title-name").click(        
    function(e){
        if(e.target.className.indexOf("btn-default")>=0){
            $(".room-title-name").html(roomName);
        }
        else if(e.target.className=="room-title-name"){
            $(".room-title-name").html(span_div);  
            name_input.innerHTML=roomName;
        }      
        else if(e.target.className.indexOf("btn-primary")>=0){
            
        }
    });
      
    var eventHandler=function(){
        bun1.removeAttribute("disabled");
    }
    name_input.addEventListener("input",eventHandler,false);
}