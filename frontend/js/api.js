let api = function(path, args, callback){
     $.ajax({
         type: 'POST',
         url: `http://localhost:8000${path}`,
         beforeSend: function(request) {
            let token = Cookies.get("token")
            if(token){
                request.setRequestHeader("token",token)
            }
         },
         data: JSON.stringify(args),
         success: callback,
         error: function(xhr){
            if(xhr.status==401){
                window.location.href = "login.html"
            }
         },
         contentType: "application/json",
         dataType: 'json'
     });
}

