var attachHandlers = function () {

    var save = document.getElementById("saveform");

    if (save != null) {
        var saveSaveButton = document.getElementById("savesave");
        var saveResetButton = document.getElementById("savereset");


        saveSaveButton.addEventListener('click', function () {
            save.setAttribute("onsubmit", "saveForm.save(this);return false;");


        });

        saveResetButton.addEventListener('click', function () {
            save.setAttribute("onsubmit", "saveForm.reset(this);return false;");


        });
    }

    var search = document.getElementById("searchform");

    if (search != null) {
        var searchSearchButton = document.getElementById("searchsearch");
        var searchResetButton = document.getElementById("searchreset");


        searchSearchButton.addEventListener('click', function () {
            search.setAttribute("onsubmit", "searchForm.search(this);return false;");
        });

        searchResetButton.addEventListener('click', function () {
            search.setAttribute("onsubmit", "searchForm.reset(this);return false;");
        });
    }


}

var init = function () {
    attachHandlers();
}

window.onload = function () {
    init();
};


//====================================================================================================================================================================================
var saveForm = {

    save: function (formData) {

      

        var newContact = {
            "firstname": formData.firstname.value.trim(),
            "familyname": formData.familyname.value.trim(),
            "mobile": formData.mobile.value.trim()
        };

        var con = new XMLHttpRequest();

        con.open("POST", '/savecontact', true);

        con.onreadystatechange = function () {
            if (con.readyState == 4 && con.status == 200) {

                document.getElementById("msg").innerHTML = "Contacted added!";

            } else if (con.status == 501) {
                document.getElementById("msg").innerHTML = "Something went wrong!";
            }
        };

        con.setRequestHeader("Content-Type", "application/json");

        con.send(JSON.stringify(newContact));



    },

    reset: function (formData) {

        formData.firstname.value = "";
        formData.familyname.value = "";
        formData.mobile.value = "";
    }

};


var searchForm = {

    search: function (formData) {


      


        var firstname = formData.firstname.value.trim();
        var familyname = formData.familyname.value.trim();

        var con = new XMLHttpRequest();


        con.open("GET", '/getcontact/' + firstname + '/' + familyname, true);

        con.onreadystatechange = function () {
            if (con.readyState == 4 && con.status == 200) {
		    var resultTable = document.getElementById("searchresult");
		    resultTable.innerHTML = "";
                var result = JSON.parse(con.responseText);
                if (result.length > 0) {

                    document.getElementById("footercontainer").style.display = "block";

                    
			  result.forEach(function (r) {
                        resultTable.innerHTML += "<tr><td>" + r.firstname + " " + r.familyname + "</td><td>" + r.mobile + "</td></tr>";
                    });
                }else{

		    	document.getElementById("footercontainer").style.display = "None";
                }


            } else if (con.status == 404) {
                  var resultTable = document.getElementById("searchresult");
		      resultTable.innerHTML = "";                
			document.getElementById("footercontainer").style.display = "None";
            }
        };
        con.send(null);

    },

    reset: function (formData) {
        formData.firstname.value = "";
        formData.familyname.value = "";
    },

    remove: function () {

    }

};
