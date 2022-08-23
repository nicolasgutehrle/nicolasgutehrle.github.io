function openPage(pageName,elmnt,color) {
    var i, tabcontent, tablinks;

 
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";

           
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
      tablinks[i].style.fontSize = "20px";
	tablinks[i].style.borderBottom = "none";

  }

    document.getElementById(pageName).style.display="block";
   
    elmnt.style.borderBottom = "thick solid #ff017d";
    elmnt.style.fontSize = "25px";


}

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();
