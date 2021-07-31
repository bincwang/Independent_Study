function login(args){
    api("/login",args,function(res){
        if(res.code){
            Cookies.set("token", res.data)
            window.location.href = "index.html"
        }else{
            alert("Sorry:"+res.data)
        }
    })
}
function check_with_database(){
    let username = document.getElementById("username_input").value;
    let password = document.getElementById("password_input").value;
    let args = {username:username, password:password}
    login(args);
};

//Click on submit2 means login
submit2.addEventListener("click",function(){
    check_with_database();
    //Check with database to see if there's a match
});
submit3.addEventListener("click",function(){
    let username = document.getElementById("username_input").value;
    let password = document.getElementById("password_input").value;
    let args = {username:username, password:password}
    api("/unregister",args,function(res){
        if(res.code){
            alert("Done!")
        }else{
            alert(res.data)
        }
    })
});


