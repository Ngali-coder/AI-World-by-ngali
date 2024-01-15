

//alert("testt")
function onClickGetSentiment(){
  console.log("see categorie button clicked");
  var tweet = document.getElementById("uiSqft20"); 
  
  var  estTweet= document.getElementById("uiTweet");

  var url = "http://127.0.0.1:5000/throw_text"; //Use this if you are NOT using nginx which is first 7 tutorials
  // var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards

  $.post(url, {
      
      tweet: tweet.value,
  },function(data, status) {
      console.log(data.text);
      estTweet.innerHTML = "<h3>" + data.text;
      console.log(status);
  });

}