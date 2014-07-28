function submForm(event) {
  
  var name = event.name;
  var clss = event.className;
  var data = event.value;

  $.ajax({
    type: "POST",
    url: "/index",
    data: clss + ',' + data
  });
}



function sqlPopUp(event) {
            
  var clss = event.className;

  $.ajax({
    type: "POST",
    url: "/sql_text",
    data: clss
  });

  window.open('/sql_text');
}

function submFilter(event) {
  
  var name = event.name;
  var data = event.value;

  $.ajax({
    type: "POST",
    url: "/filter",
    data: name + ',' + data
  });
}
