const audio = document.getElementById("myAudio");
let num1 = 0;
let num2 = 0;
let first_carry = 0;
let second_carry = 0;
let third_carry = 0;
let first_answer = 0;
let second_answer = 0;
let third_answer = 0;
let operator = "+";

function generate_equation() {
    num1 = Math.floor(Math.random() * (100 - 10) + 10);
    num2 = Math.floor(Math.random() * (100 - 10) + 10);
    //IMPORTANT, I NEED TO ADD CODE HERE
    document.getElementById("num1").innerHTML = num1;
    document.getElementById("num2").innerHTML = num2;
    document.getElementById("first_carry").innerHTML = "";
    document.getElementById("second_carry").innerHTML = "";
    document.getElementById("third_carry").innerHTML = "";
    document.getElementById("first_answer").innerHTML = "";
    document.getElementById("second_answer").innerHTML = "";
    document.getElementById("third_answer").innerHTML = "";
};

submit1.addEventListener("click",function(){
    first_carry =parseInt(document.getElementById("first_carry").value)||0;
    second_carry =parseInt(document.getElementById("second_carry").value)||0;
    third_carry =parseInt(document.getElementById("third_carry").value)||0;
    first_answer =parseInt(document.getElementById("first_answer").value)||0;
    second_answer =parseInt(document.getElementById("second_answer").value)||0;
    third_answer =parseInt(document.getElementById("third_answer").value)||0;
    operator = document.getElementById("operator").innerHTML;

    args = {
            num1: num1,
            num2: num2,
            operator: operator,
            answer:[third_answer,second_answer,first_answer],
            carry:[third_carry, second_carry, first_carry],
    }

    // check answer
    api("/submit", args, function(res){
        // if correct
        if(!res.code){
            alert("Answers are incorrect, please refill those blanks and submit again: "+res.data);
        }
        api("/info",{},function(res2){
            if(res2.code){
                document.getElementById("score_update").innerHTML = res2.data.score;
            }
        })
        generate_equation();
    })
});

generate_equation()
