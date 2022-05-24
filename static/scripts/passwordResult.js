
//    var host = "https://knowyourpassword.pythonanywhere.com/api/v1/"
   var host = "http://127.0.0.1:5000/api/v1/"
   
   function checkPassword() {
   
       document.getElementsByName('source').forEach(function(ele, idx) {
           ele.style.color = "white";
       })
       document.getElementById('Error').style.display = "none";
       document.getElementById("searchPwnedPasswords").disabled = true;
   
       var password = document.getElementById("Password").value;
       var loading = '<div class="center"><div class="wave"></div><div class="wave"></div><div class="wave"></div><div class="wave"></div><div class="wave"></div><div class="wave"></div><div class="wave"></div><div class="wave"></div><div class="wave"></div><div class="wave"></div></div>'
   
       if (password.length == 0) {
           document.getElementById("ErrorMessage").innerHTML = "That's not a real password!";
   
           showHide("Error")
       } else {
           document.getElementById('Error').style.display = "none";
           document.getElementsByName('source').forEach(function(ele, idx) {
               ele.innerHTML = loading;
           })
           document.getElementById("ErrorMessage").innerHTML = "";
   
           setTimeout(function() {
               checkhaveibeenpwned((hex_sha1(password)).toUpperCase());
           }, 100);
       }
   }
   
   async function checkhaveibeenpwned(hashPassword) {
   
       var url = host + "haveibeenpwned/" + hashPassword.substring(0, 5);
   
       fetch(url).then(function(response) {
           return response.json();
       }).then(function(json) {
           if (json.status == 429) {
               twoManyRequest();
           } else if (json.status == 200) {
               checkResult(json, hashPassword, "haveibeenpwned").then(function() {
                   checkrockyou(hashPassword);
               });
           } else {
               document.getElementById("haveibeenpwned").innerHTML = "Error";
               checkrockyou(hashPassword);
           }
       });
   }
   
   async function checkrockyou(hashPassword) {
   
       var url = host + "rockyou/" + hashPassword.substring(0, 5);
   
       fetch(url).then(function(response) {
           return response.json();
       }).then(function(json) {
           if (json.status == 429) {
               twoManyRequest();
           } else if (json.status == 200) {
               checkResult(json, hashPassword, "rockyou").then(function() {
                   topmillion(hashPassword);
               });
           } else {
               document.getElementById("rockyou").innerHTML = "Error";
               topmillion(hashPassword);
           }
       });
   }
   
   async function topmillion(hashPassword) {
   
       var url = host + "topmillion/" + hashPassword.substring(0, 5);
       setTimeout(function() {
           fetch(url).then(function(response) {
               return response.json();
           }).then(function(json) {
               if (json.status == 429) {
                   twoManyRequest();
               } else if (json.status == 200) {
                   checkResult(json, hashPassword, "topmillion").then(function() {
                       document.getElementById("searchPwnedPasswords").disabled = false;
                   });
               } else {
                   document.getElementById("topmillion").innerHTML = "Error";
                   document.getElementById("searchPwnedPasswords").disabled = false;
               }
           });
       }, 1000);
   }
   
   
   function twoManyRequest() {
   
       document.getElementsByName('source').forEach(function(ele, idx) {
           ele.style.color = "white";
           ele.innerHTML = 'Error';
       })
       document.getElementById("ErrorMessage").innerHTML = "Too many request";
   
       showHide("Error")
   }
   
   
   function showHide(id) {
   
       if (document.getElementById) {
           var divId = document.getElementById(id);
   
           $(divId).fadeIn("slow");
   
           document.getElementById("searchPwnedPasswords").disabled = false;
       }
       return false;
   }
   
   async function checkResult(json, hashPassword, id) {
   
       hashes = json.hashes;
   
       if(hashes.length == 0){
           document.getElementById(id).innerHTML = "Not Found";
           document.getElementById(id).style.color = "green";
       }
   
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