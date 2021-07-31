function store_into_database(){
    let username = document.getElementById("username_input").value;
    let password = document.getElementById("password_input").value;
    let args = {username: username, password: password}
    api("/register",args,function(res){
        if(res.code){
            alert("Congratulation!");
            login(args)
        }else{
            alert("Sorry: "+res.data)
        }
    })
};

submit1.addEventListener("click",function(){
    store_into_database();
});
