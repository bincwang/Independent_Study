function get_info(){
    let token = Cookies.get("token")
    if(token){
        info = api("/info",{},function(res){
           if(res.code==0){
               Cookies.remove("token")              
               alert("Please login again!")
               window.location.href = "login.html";
           }else{
                //alert("welcome! "+res.data.username);
                document.getElementById("score_update").innerHTML = res.data.score;
                new_string = "Welcome " + res.data.username;
                document.getElementById("username").innerHTML = new_string;
                return
           }
        })
    }else{
        alert("Please login first!")
        window.location.href = "login.html";
    }
}

logout_button.addEventListener("click",function(){
    api("/logout",{},function(res){
        if(res.code){
            alert("Done")
            window.location.href = "login.html"
        }else{
            alert(res.data)
        }
    })
});

get_info()
