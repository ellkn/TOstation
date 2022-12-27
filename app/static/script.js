function myFunctionUser() {
    let input, filter, table, tr, td, i;
    input = document.getElementById("myInputUser");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTableUser");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0];
      if (td) {
        if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }       
    }
  }

  function myFunction() {
    let input, filter, table, tr, td, i;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[4];
      if (td) {
        if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }       
    }
  }

  function myFunctionT() {
    let input, filter, table, tr, td, i;
    input = document.getElementById("myInputT");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTableT");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[7];
      if (td) {
        if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }       
    }
  }

// let f = document.getElementById["f"], s = document.getElementById('user')
// o = s.querySelectorAll("option"),
// inp = document.getElementById('search'),
// reg;
// inp.oninput = function() {
//   reg = new RegExp(this.value, "ig"); 
//   s.options.length = 0;
//   for (var i=0; i<o.length; i++)  {
//      reg.test(o[i].text) && s.options.add(o[i]);
//      reg.lastIndex = 0;
//   }
// }