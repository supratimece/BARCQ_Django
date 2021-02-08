function addItem(candidate){
    var ul = document.getElementById("dynamic-list");
    // var candidate = document.getElementById("candidate");
    var table = document.getElementById("savedTable")
    var li = document.createElement("li");
    var a1 = document.createElement("a");
    var a2 = document.createElement("a");
    var i = document.createElement("i");
    var tr = document.createElement("tr");
    var td1 = document.createElement("td");
    var td2 = document.createElement("td");
    i.setAttribute('class', "fa fa-trash");
    li.setAttribute('id',candidate);
    li.style.color = "white";
    i.style.color = "red";
    a2.setAttribute("href", "#");
    //li.appendChild(document.createTextNode(candidate));
    a1.appendChild(document.createTextNode(candidate));
    a2.appendChild(i);
    li.appendChild(a1);
    td1.appendChild(li);
    td2.appendChild(a2);
    tr.appendChild(td1, td2);
    table.appendChild(tr);

    // ul.appendChild(li);
}

function removeItem(candidate){
    var ul = document.getElementById("dynamic-list");
    // var candidate = document.getElementById("candidate");
    var item = document.getElementById(candidate.value);
    ul.removeChild(item);
}