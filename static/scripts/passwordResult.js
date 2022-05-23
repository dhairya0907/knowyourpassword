async function checkPassword() {

    document.getElementById('Error').style.display = "none";
    document.getElementById("searchPwnedPasswords").disabled = true;

    var password = document.getElementById("Password").value;
    var loading = '<div class="center"><div class="wave"></div><div class="wave"></div><div class="wave"></div><div class="wave"></div><div class="wave"></div><div class="wave"></div><div class="wave"></div><div class="wave"></div><div class="wave"></div><div class="wave"></div></div>'

    if (password.length == 0) {
        document.getElementById("ErrorMessage").innerHTML = "That's not a real password!";

        showHide("Error")
    } else {
        document.getElementById('Error').style.display = "none";
        document.getElementById("haveibeenpwned").innerHTML = loading;
        document.getElementById("rockyou").innerHTML = loading;
        document.getElementById("ErrorMessage").innerHTML = "";

        setTimeout(async function() {
            hashPassword = await (hex_sha1(password)).toUpperCase();
            checkhaveibeenpwned(hashPassword);
        }, 100);
    }
}

async function checkhaveibeenpwned(hashPassword) {

    var url = "https://knowyourpassword.pythonanywhere.com/api/v1/haveibeenpwned/" + hashPassword.substring(0, 5);
    var response = await httpGet(url);
    var json = JSON.parse(response);

    if (json.status == 429) {
        await twoManyRequest();
    } else if (json.status == 200) {
        await checkResult(json, hashPassword, "haveibeenpwned");
        await checkrockyou(hashPassword);
    } else {
        document.getElementById("haveibeenpwned").innerHTML = "Error";

        await checkrockyou(hashPassword);
    }
}

async function checkrockyou(hashPassword) {

    var url = "https://knowyourpassword.pythonanywhere.com/api/v1/rockyou/" + hashPassword.substring(0, 5);
    var response = await httpGet(url);
    var json = JSON.parse(response);

    if (json.status == 429) {
        await twoManyRequest();
    }
    if (json.status == 200) {
        await checkResult(json, hashPassword, "rockyou");

        document.getElementById("searchPwnedPasswords").disabled = false;
    } else {
        document.getElementById("rockyou").innerHTML = "Error";
        document.getElementById("searchPwnedPasswords").disabled = false;
    }

}


async function twoManyRequest() {

    document.getElementsByName('source').forEach(function(ele, idx) {
        ele.innerHTML = 'Error';
    })
    document.getElementById("ErrorMessage").innerHTML = "Too many request";

    showHide("Error")
}


async function showHide(id) {

    if (document.getElementById) {
        var divId = document.getElementById(id);

        $(divId).fadeIn("slow");

        document.getElementById("searchPwnedPasswords").disabled = false;
    }
    return false;
}


async function httpGet(theUrl) {

    var xmlHttp = new XMLHttpRequest();

    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);

    return xmlHttp.responseText;
}


async function checkResult(json, hashPassword, id) {

    hashes = json.hashes;

    for (var i = 0; i < hashes.length; i++) {
        if (hashes[i] == hashPassword.slice(5)) {
            document.getElementById(id).innerHTML = "Found";
            document.getElementById(id).style.color = "red";
            break;
        } else {
            document.getElementById(id).innerHTML = "Not Found";
            document.getElementById(id).style.color = "green";
        }
    }
}