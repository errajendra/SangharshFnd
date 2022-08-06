$(document).on('click', '#contactSubmmit', function(e) {
    var name = document.getElementById("name").value;
    var email = document.getElementById("email").value;
    var mobile_nomber = document.getElementById("mobile_nomber").value;
    var message = document.getElementById("message").value;
    if(validateEmail(email) && name != ""){
        $.ajax({
            type: 'post',
            url: 'ajax/',
    
            data : {
                action: "contact",
                name: name,
                email: email,
                message: message,
                mobile_nomber: mobile_nomber
            },
            
            success: function(data) {
                document.getElementById("name").value="";
                document.getElementById("email").value="";
                document.getElementById("message").value="";
                document.getElementById("mobile_nomber").value="";
                alert("Successfully Submitted...!");
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) { 
                alert("Status: " + textStatus + ", fill correct form...");
            }  
        });
    } else {
        alert("Enter Vailied Name Email id..");
    }
});


// email vailidator
function validateEmail(email){
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

