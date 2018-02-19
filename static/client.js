

displayview = function(){
	//get the token in the local storage
   var token =localStorage.getItem("loggedinuser");

   var con = new XMLHttpRequest();

   con.open("GET", '/getdatabytoken/'+token, true);

   con.onreadystatechange = function () {
     // check if this token exists in our server
     if (con.readyState == 4 && con.status == 200) {
      // if it exists, show the profile view
      document.getElementById("navcontainer").innerHTML=document.getElementById("navview").innerHTML;
      var idnavbar = localStorage.getItem("navbar");
      clicknavbutton(idnavbar);
     }else{
       // else show the welcome view
       document.getElementById("maincontainer").innerHTML=document.getElementById("welcomeview").innerHTML;
     }
   };
   con.send(null);
};

// Function that validates the form
validateForm = function() {

		// Passwords inputs and message to display
	    var password = document.getElementById("passwordsignup");
	    var repeatPassword = document.getElementById("repeatpassword");

	    var X = 6;

	    // Passwords validation, if both are the same ---------------------------
	    if (password.value.trim() != repeatPassword.value.trim()){
			repeatPassword.setCustomValidity("Password are not the same!");
	    	password.focus();
	    	return false;
	    }
		// Characters long validation, if both passwords are longer than certain value ---------
	    else if(password.value.trim().length < X || repeatPassword.value.trim().length < X){
			password.setCustomValidity("Password is too short!");
			return false;
		}else{
			return true;
		}

	};

//Sign-up function called when the user submit the form to sign up
signup = function(){
	var formData = document.forms["sign-up-form"];
	if(validateForm()){
		// create a new JSON object
		var newProfile = {
				"email": formData.emailsignup.value.trim(),
				"password": formData.passwordsignup.value.trim(),
				"firstname": formData.firstname.value.trim(),
				"familyname": formData.familyname.value.trim(),
				"gender": formData.gender.value.trim(),
				"city": formData.city.value.trim(),
				"country": formData.country.value.trim()
		};
		// try to sign up with this contact
		var result = serverstub.signUp(newProfile);

    var con = new XMLHttpRequest();
    // open a put request to the server to sign up
    con.open("PUT", '/signup', true);

    con.onreadystatechange = function () {
        if (con.readyState == 4 && con.status == 200) {
          // show the profile view and store the token into the local storage
    			document.getElementById("navcontainer").innerHTML=document.getElementById("navview").innerHTML;
    			document.getElementById("maincontainer").innerHTML=document.getElementById("profileview").innerHTML;
          // open a new request to sign in
          con.open("PUT", '/signin', true);
          // create the JSON parameters with email and password
          var id = {
      				"email": newProfile.email,
      				"password": newProfile.password,
      		};
          con.onreadystatechange = function () {
            data = JSON.parse(con.responseText).data;
            localStorage.setItem("loggedinuser",data);
      			// display profile of the current user
      			displayprofile();
          }
          con.setRequestHeader("Content-Type", "application/json");
          //send the request
          con.send(JSON.stringify(id));

        } else {
          	// show an error message
          var email= document.getElementById("emailsignup");
          email.setCustomValidity("This email address already exists!");
        }
    };

    con.setRequestHeader("Content-Type", "application/json");
    // send the signup request
    con.send(JSON.stringify(newProfile));
	}
	formData.reportValidity();
	return false;
}

//Sign-in function called when the user submit the form to login
signin = function(){
		var formData = document.forms["login-form"];
		var message = document.getElementById("message");
		//receive the token from the server and see if the user exist
		var result

    // open a new request to sign in
    con.open("PUT", '/signin', true);
    // create the JSON parameters with email and password
    var logform = {
        "email": formData.emaillogin.value.trim(),
        "password": formData.passwordlogin.value.trim(),
    };
    con.onreadystatechange = function () {
      // if the user exist display his profile view and store the token in the local storage
      if (con.readyState == 4 && con.status == 200) {
  			document.getElementById("navcontainer").innerHTML=document.getElementById("navview").innerHTML;
  			document.getElementById("maincontainer").innerHTML=document.getElementById("profileview").innerHTML;
        data = JSON.parse(con.responseText).data;
  			localStorage.setItem("loggedinuser",data);
        // display profile of the current user
        displayprofile();
      }else {
        // else display an error message
    		var username = document.getElementById("emaillogin");
    		username.setCustomValidity(JSON.parse(con.responseText).message);
      }
    }
    con.setRequestHeader("Content-Type", "application/json");
    //send the request
    con.send(JSON.stringify(logform));

		formData.reportValidity();
		return false;
}

// Clear custom validity form when the user is written in the field
clearcustomvalidity = function(field){
	field.setCustomValidity("")
}

//Sign-out function called when the user wants to signout from the system
signout = function(){
	var token =localStorage.getItem("loggedinuser");
	serverstub.signOut(token);
	localStorage.removeItem("loggedinuser");
	document.getElementById("navcontainer").innerHTML= "";
	document.getElementById("maincontainer").innerHTML=document.getElementById("welcomeview").innerHTML;

	 // set homenav by default in the navbar
	  localStorage.setItem('navbar',"homenav");

}

//Function to validate the forms in account view
validatePassForm = function() {

		// Passwords inputs and message to display
	    var newpass = document.getElementById("newpass");
	    var repeatnewpass= document.getElementById("repeatnewpass");

	    var messagePass = document.getElementById("messagePass");
	    var X = 6;

	    // Passwords validation ----------------------------------
	    if (newpass.value.trim() != repeatnewpass.value.trim()){
			repeatnewpass.setCustomValidity("The new pass are not the same!");
	    	newpass.focus();
	    	return false;
	    }
	    else{

	    	// Characters long validation ----------------------------
		    if(newpass.value.trim().length < X || repeatnewpass.value.trim().length < X){
				newpass.setCustomValidity("The new pass is too short!");
		    	return false;
		    }
	    	return true;
	    }
	};

//Function that triggers the password change
changePassword = function(){
	var token = localStorage.getItem("loggedinuser");
	var formData = document.forms["changepass-form"];

	if(validatePassForm()){
		var oldPassId = document.getElementById("oldpass");
		var old_pass = formData.oldpass.value.trim();
		var new_pass = formData.newpass.value.trim();

		// try to sign up with this contact
		var result = serverstub.changePassword(token, old_pass, new_pass);
		// show an error message
		if(!result.success){
			oldPassId.setCustomValidity(result.message);
		}else{
			messagePass.innerText = "The password was changed successfully!";
		}
	}
	formData.reportValidity();
	return false;
}

//Function that triggers different behaviors depending which button is clicked from the tab
clicknavbutton = function(id){

	// Variables
	var button_nav = document.getElementById(id);
	var token = localStorage.getItem("loggedinuser");
	localStorage.setItem("navbar",id);

	// To change the active section of the bar
	if(!button_nav.classList.contains("active")){

		var active_button = document.getElementsByClassName("active")[0];
		active_button.classList.remove("active");

		button_nav.classList.add("active");
	}

	if(id == "homenav"){ // If the home button is active
		document.getElementById("maincontainer").innerHTML=document.getElementById("profileview").innerHTML;
		// display profile of the current user
		displayprofile();
	}
	else if(id == "browsenav"){ // If the browse button is active
		document.getElementById("maincontainer").innerHTML=document.getElementById("profileview").innerHTML;

		// display profile of the current user
		//displaypanel.profile();
		document.getElementById("browse").style.display = "block";
		document.getElementById("home").style.display = "none";
	}
	else if(id == "accountnav"){ // If the account button is active

		document.getElementById("maincontainer").innerHTML=document.getElementById("accountview").innerHTML;

	}
	else{ // Error
		document.getElementById("maincontainer").innerHTML="Sorry, this address doesn't exit";
	}
	return false;
}

// Show the profile of a person depending on the token in parameter
displayprofile = function(email=""){

	var token = localStorage.getItem("loggedinuser");
	// Get the data of the user from the server depending on his token
	if(email==""){
		var result= serverstub.getUserDataByToken(token);
	}else{
		var result= serverstub.getUserDataByEmail(token,email);
	}

	if(result.success){
		// display all the data of the user
		document.getElementById("homeusername").innerText=result.data.firstname +" " + result.data.familyname;
		document.getElementById("homegender").innerText=result.data.gender;
		document.getElementById("homeemail").innerText=result.data.email;
		document.getElementById("homecity").innerText=result.data.city;
		document.getElementById("homecountry").innerText=result.data.country;
	}
	displaymessages();
}

// methode to post a message to a wall
postmessage = function(){
	var message = document.getElementById("postmessage").value.trim();
	// if the message is not null, send it to the server
	if(message!=""){
		var token = localStorage.getItem("loggedinuser");
		var email = document.getElementById("homeemail").innerText;
		serverstub.postMessage(token, message, email);
		document.getElementById("postmessage").value="";
	}
	return false;
}

/*display messages of all the current profile -- also called to refresh a page*/
displaymessages= function(){
	var email = document.getElementById("homeemail").innerText;
  	// get the token of the current user
	var token = localStorage.getItem("loggedinuser");
	var messages = serverstub.getUserMessagesByEmail(token,email);


// get the email of the current user with his token
	var currentuseremail = serverstub.getUserDataByToken(token).data.email;
	document.getElementById("messages").innerHTML="";
	var result=document.getElementById("messages");
	for (var i=0; i<messages.data.length;i++){

		//show messages and change style depending if the email is the current user's email
		if(messages.data[i].writer==currentuseremail){
			result.innerHTML+="<div class='postername'><span id='postername"+i+"'></span></div><div class='postermessage'><span id='postermessage"+i+"'></span></div>";
		}
		else{
			result.innerHTML+="<div class='posternameothers'><span id='postername"+i+"'></span></div><div class='postermessageothers'><span id='postermessage"+i+"'></span></div>";
		}
		document.getElementById("postername"+i).innerText=messages.data[i].writer;
		document.getElementById("postermessage"+i).innerText=messages.data[i].content;

	}

}

// find the profile with the username given by the input
searchprofile = function(){
	var email = document.getElementById("search").value.trim();
	var token = localStorage.getItem("loggedinuser");
	var result=serverstub.getUserMessagesByEmail(token,email);
	if(result.success){// if the user exists
		//show profile
		displayprofile(email);
		document.getElementById("home").style.display = "block";
		document.getElementById("messageusername").innerText="";
	}else{

		var message =serverstub.getUserMessagesByEmail(token,email).message;
		var emailId=document.getElementById("search");
		emailId.setCustomValidity(message);
		emailId.reportValidity();
		document.getElementById("home").style.display = "none";
	}
}


// Main function- Called when the page is loading
window.onload = function(){

	displayview();

}
