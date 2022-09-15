var first, second, disp = "";


function findConnection(){
    first = document.getElementById("firstword").value;
    second = document.getElementById("secondword").value;
    console.log(first);
    console.log(second);

    disp = "No connection between the terms " + first + " and " + second;
    document.getElementById("connection").innerHTML = disp;
}