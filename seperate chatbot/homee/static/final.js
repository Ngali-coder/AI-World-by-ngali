//function onClickedEstimatePrice() {
//    console.log("Estimate sales button clicked");
//    var month3 = document.getElementById("uiSqft3");
//    var month2 = document.getElementById("uiSqft2");
//    var month1 = document.getElementById("uiSqft1");
//    var estSales = document.getElementById("uiEstimatedPrice");
//
//    var url = "http://127.0.0.1:5000/forecast_sales"; //Use this if you are NOT using nginx which is first 7 tutorials
//    // var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
//
//    $.post(url, {
//        month3: parseFloat(month3.value),
//        month2: parseFloat(month2.value),
//        month1: parseFloat(month1.value),
//    },
//      function (data, status) {
//        console.log(data.estimated_sales);
//        estSales.innerHTML = "<h2>" + data.estimated_sales.toString() + " units</h2>";
//
//        console.log(status);
//      }
//    );
//}


function loginn() {
   
    var managerUsername = document.getElementById("input1");
    var managerPassword = document.getElementById("input2");

    var url = "http://127.0.0.1:5000/forecast_sales"; //Use this if you are NOT using nginx which is first 7 tutorials
    // var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
  
    $.post(url, {
        managerUsername: managerUsername.value,
        managerPassword: managerPassword.value,
    });
}


function Registers() {
 
    var managerFirstName = document.getElementById("input3");
    var managerLastName = document.getElementById("input4");
    var managerEmail = document.getElementById("input5");
    var managerPassword = document.getElementById("input6");

    var url = "http://127.0.0.1:5000/forecast_sales"; //Use this if you are NOT using nginx which is first 7 tutorials
    // var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards

        $.post(url, {
            managerFirstName: managerFirstName.value,
            managerLastName: managerLastName.value,
            managerEmail: managerEmail.value,
            managerPassword: managerPassword.value,
    });
}

function registerClient() {
 
    var clientName = document.getElementById("input9");
    var clientEmail = document.getElementById("input10");
    var clientPassword = document.getElementById("input11");

    var url = "http://127.0.0.1:5000/forecast_sales"; //Use this if you are NOT using nginx which is first 7 tutorials
    // var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards

        $.post(url, {
            clientName: clientName.value,
            clientEmail: clientEmail.value,
            clientPassword: clientPassword.value,
    });
}

function loginClient() {
 
    var clientName = document.getElementById("input7");
    var clientPassword = document.getElementById("input8");

    var url = "http://127.0.0.1:5000/forecast_sales"; //Use this if you are NOT using nginx which is first 7 tutorials
    // var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards

        $.post(url, {
            clientName: clientName.value,
            clientPassword: clientPassword.value,
    });
}

//alert("test")