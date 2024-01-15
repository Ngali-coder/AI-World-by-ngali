// function getBathValue() {
//     var uiBathrooms = document.getElementsByName("uiBathrooms");
//     for(var i in uiBathrooms) {
//       if(uiBathrooms[i].checked) {
//           return parseInt(i)+1;
//       }
//     }
//     return -1; // Invalid Value
//   }
  
  // function getBHKValue() {
  //   var uiBHK = document.getElementsByName("uiBHK");
  //   for(var i in uiBHK) {
  //     if(uiBHK[i].checked) {
  //         return parseInt(i)+1;
  //     }
  //   }
  //   return -1; // Invalid Value
  // }
//  alert("testt")
  function onClickedEstimatePrice() {
    console.log("Estimate price button clicked");
    var prix = document.getElementById("uiSqft");
    var prix_achat =document.getElementById("uiBHK");
    var categorie = document.getElementById("uiBathrooms");
    var code = document.getElementById("uiLocations");
    var estPrice = document.getElementById("uiEstimatedPrice");
  
    var url = "http://127.0.0.1:5000/predict_save_price"; //Use this if you are NOT using nginx which is first 7 tutorials
    // var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
  
    $.post(url, {
        prix: parseFloat(prix.value),
        prix_achat: prix_achat,
        categorie: categorie,
        code: code.value
    },function(data, status) {
        console.log(data.estimated_price);
        estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " FCFA</h2>";
        console.log(status);
    });
  }
  
  function onPageLoad() {
    console.log( "document loaded" );
    var url = "http://127.0.0.1:5000/get_code_names"; // Use this if you are NOT using nginx which is first 7 tutorials
    // var url = "/api/get_location_names"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
    $.get(url,function(data, status) {
        console.log("got response for get_code_names request");
        if(data) {
            var code = data.code;
            var uiLocations = document.getElementById("uiLocations");
            $('#uiLocations').empty();
            for(var i in code) {
                var opt = new Option(code[i]);
                $('#uiLocations').append(opt);
            }
        }
    });
  }
  
  window.onload = onPageLoad;