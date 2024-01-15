//alert("testt")

  function onClickedEstimatePrice() {
    console.log("Estimate sales button clicked");
    var month3 = document.getElementById("uiSqft3");
    var month2 = document.getElementById("uiSqft2");
    var month1 = document.getElementById("uiSqft1");
    var estSales = document.getElementById("uiEstimatedPrice");
  
    var url = "http://127.0.0.1:5000/forecast_sales"; //Use this if you are NOT using nginx which is first 7 tutorials
    // var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
  
    $.post(url, {
        month3: parseFloat(month3.value),
        month2: parseFloat(month2.value),
        month1: parseFloat(month1.value),
    },
      function (data, status) {
        console.log(data.estimated_sales);
        estSales.innerHTML = "<h2>" + data.estimated_sales.toString() + " units</h2>";
        
        console.log(status);
      }
    );
  }
  


  // function onClickedSeeCategorieId() {
  //   console.log("see categorie button clicked");
  //   var start_date = document.getElementById("uiSqft33"); 
  //   var end_date = document.getElementById("uiSqft32"); 
  //   var estId = document.getElementById("uiSeeId");
  
  //   var url = "http://127.0.0.1:5000/get_categorie_id"; //Use this if you are NOT using nginx which is first 7 tutorials
  //   // var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
  
  //   $.post(url, {
  //       start_date: start_date.value,
  //       end_date: end_date.value,
  //   },function(data, status) {
  //       console.log(data.id_categorie);
  //       estId.innerHTML = "<h2>" + data.id_categorie;
  //       console.log(status);
  //   });

  // }

  function onClickedSeeCategorieId() {
    console.log("see categorie button clicked");
    var start_date = document.getElementById("uiSqft33"); 
    var end_date = document.getElementById("uiSqft32"); 
    var variable = document.getElementById("uiSqft15");
    var estId = document.getElementById("uiSeeId");
  
    var url = "http://127.0.0.1:5000/get_categorie_id"; //Use this if you are NOT using nginx which is first 7 tutorials
    // var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
  
    $.post(url, {
        start_date: start_date.value,
        end_date: end_date.value,
        variable: variable.value,
    },function(data, status) {
        console.log(data.id_categorie);
        estId.innerHTML = "<h2>" + data.id_categorie;
        console.log(status);
    });

  }


  function onClickedGet_categorie_name() {
    console.log("see categorie button clicked");
    var catID = document.getElementById("uiSqft4"); 
    var estCN = document.getElementById("uiSeeCN");

  
    var url = "http://127.0.0.1:5000/get_categorie_name"; //Use this if you are NOT using nginx which is first 7 tutorials
    // var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
  
    $.post(url, {
        categorie_id: parseInt(catID.value),

    },function(data, status) {
        console.log(data.category_name);
        estCN.innerHTML = "<h6>" + data.category_name;
        console.log(status);
    });
 
  }

function onClickedGet_client_name() {
    console.log("see client button clicked");
    var catID = document.getElementById("uiSqft4"); 
    var estCLN = document.getElementById("uiSeeCLN");  
    var url = "http://127.0.0.1:5000/get_client_name"; //Use this if you are NOT using nginx which is first 7 tutorials
    // var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
  
    $.post(url, {
        categorie_id: parseInt(catID.value),

        
    },function(data, status) {
        console.log(data.client_name);
        estCLN.innerHTML = "<h6>" + data.client_name;
        console.log(status);
        
    });

  }

  function onClickPossibility() {
    console.log("possibility button clicked");
    var catID = document.getElementById("uiSqft4");
    var expected_sales = document.getElementById("uiSqft31");
    var estimate = document.getElementById("uiSqft9");
    var estPoss = document.getElementById("uiPossible");  
    var url = "http://127.0.0.1:5000/possibility"; //Use this if you are NOT using nginx which is first 7 tutorials
    // var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
  
    $.post(url, {
      categorie_id: parseInt(catID.value),
      expected_sales: parseFloat(expected_sales.value),
      estimated_sales: parseFloat(estimate.value),

  
    },function(data, status) {
        console.log(data.possibility_check);
        estPoss.innerHTML = "<h6>" + data.possibility_check;
        console.log(status);
        
    });

  }







function openPopup() {
  popup.classList.add("open-popup");
  var expected_sales = document.getElementById("uiSqft31");
  var estimate = document.getElementById("uiSqft9");
  var estpPoss = document.getElementById('uipossible');

  if (expected_sales > estimate) {
    possibility = "Impossible";
    // console.log("impossible")
  } else {
    possibility = "possible";
    // console.log("possible")
  }
  $.post(url, {
    // categorie_id: parseInt(catID.value),

    
},function(data, status) {
    console.log(data.possibility);
    estpPoss.innerHTML = "<h6>" + data.possibility;
    console.log(status);
    
});
  
  // estpPoss.innerHTML = possibility
  // console.log(possibility)
  
}
function closePopup() {
  popup.classList.remove("open-popup");
}

  // function onClickedSeeStatistics() {
  //   console.log("See Statistics button clicked");
  //   var expected_sales = document.getElementById("uiSqft31");    
  //   var eststat = document.getElementById("SeeStat");
  
  //   expected_sales: expected_sales.value;
    
  // }

// const text1 = document.getElementById("tbuser");
// const btn1 = document.getElementById("btn1");
// const out1 = document.getElementById("uiSeeCLN");

// function fun1() {
//   out1.innerHTML = text1.value;
// }

// btn1.addEventListener("click", fun1);