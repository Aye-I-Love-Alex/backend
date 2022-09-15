
var first, second, disp = "";

function findConnection(){
//    const spawner = require('child_process').spawn
    first = document.getElementById("firstword").value;
    second = document.getElementById("secondword").value;
    console.log(first);
    console.log(second);
    disp = "No connection between the terms " + first + " and " + second;
    document.getElementById("connection").innerHTML = disp;
//    const python_process = spawner('python', ['./comparator.py', "hello"]);
//    python_process.stdout.on('data', (data) => {
//        console.log(data.toString());
//    })
}