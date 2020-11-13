htmlstart = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {
  box-sizing: border-box;
}

#myInput {
  background-image: url('https://www.w3schools.com/css/searchicon.png');
  background-position: 10px 10px;
  background-repeat: no-repeat;
  width: 100%;
  font-size: 16px;
  padding: 12px 20px 12px 40px;
  border: 1px solid #ddd;
  margin-bottom: 12px;
}

body {
  font-size: 100%;
}
a:link {
  text-decoration: none;
}
a:visited {
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
a:active {
  text-decoration: underline;
}

.links {
  font-size: 0.7em;
}
.kritzelkaffee-div {
  width: 310px;
  margin: 5px;
  display: inline-block;
  vertical-align: top;
}
.kritzelkaffee-table {
  border: 1px solid grey;
}
.kritzelkaffee-table td {
  margin: 5px;
}
.kritzelkaffee-table-date {
  text-align: center;
}
.kritzelkaffee-table-name {
  text-align: center;
}
.kritzelkaffee-table-img img {
  width: 300px;
}
.kritzelkaffee-table-text {
  text-align: left;
}
</style>
</head>
<body>

<h2>KritzelKaffees</h2>

<div>
<p>
Charakter-K&ouml;pfe, unendliche Vielfalt. Wir schreiben das Jahr 2020. Dies sind die Abenteuer des Gestruepps, das mit seiner Kreativit&auml;t schon seit über 500 Tagen unterwegs ist, um G&auml;ste zum Kaffee einzuladen. 
Dabei kritzelt das Gestruepp immer G&auml;ste, die nie zuvor ein Mensch beim KritzelKaffee gesehen hat.
</p>
<p class="links">
Alle Bilder entstammen datGestruepps Feder und sind nicht ohne Nachfrage zu verwenden.</br>
Twitter: <a href="https://twitter.com/datGestruepp">https://twitter.com/datGestruepp</a></br>
Instagram: <a href="https://www.instagram.com/datgestruepp">https://www.instagram.com/datgestruepp/</a></br>
</p>
</div>
<input type="text" id="myInput" onkeyup="filterKaffee()" placeholder="Suche nach einem Gast..." title="Namen hier eingeben">

<div id="container">
"""
#htmlfile.write("<div class=\"kritzelkaffee-div\">\n")
#htmlfile.write("<table class=\"kritzelkaffee-table\">\n")
#htmlfile.write("<tr><td class=\"kritzelkaffee-table-date\"><a href='https://twitter.com/datGestruepp/status/" + k.id + "'>Tweet vom "+k.date+"</a></td></tr>\n")
#htmlfile.write("<tr><td class=\"kritzelkaffee-table-name\">"+k.name+"</td></tr>\n")
#htmlfile.write("<tr><td class=\"kritzelkaffee-table-img\"><img src=\"placeholder.svg\" data-src='"+k.imglink+"'></td></tr>\n")
#htmlfile.write("<tr><td class=\"kritzelkaffee-table-text\">"+k.text+"</td></tr>\n")
#htmlfile.write("</table>\n")
#htmlfile.write("</div>\n")
htmlend = """
</div>

<script>
/**
* Tests if the element is visible (within the visible part of the page)
* It's enough that the top or bottom edge of the element are visible
*/
function isVisible(elem) {

    let coords = elem.getBoundingClientRect();

    let windowHeight = document.documentElement.clientHeight;

    // top elem edge is visible OR bottom elem edge is visible
    let topVisible = coords.top > 0 && coords.top < windowHeight;
    let bottomVisible = coords.bottom < windowHeight && coords.bottom > 0;

    return topVisible || bottomVisible;
}

/**
A variant of the test that considers the element visible if it's no more than
one page after/behind the current screen.

function isVisible(elem) {

    let coords = elem.getBoundingClientRect();

    let windowHeight = document.documentElement.clientHeight;

    let extendedTop = -windowHeight;
    let extendedBottom = 2 * windowHeight;

    // top visible || bottom visible
    let topVisible = coords.top > extendedTop && coords.top < extendedBottom;
    let bottomVisible = coords.bottom < extendedBottom && coords.bottom > extendedTop;

    return topVisible || bottomVisible;
}
*/

function showVisible() {
    let i = 0;
    for (let img of document.querySelectorAll('img')) {
        let realSrc = img.dataset.src;
        if (!realSrc) continue;

        if (isVisible(img)) {
            // disable caching

            img.src = realSrc;

            img.dataset.src = '';
        }
        i++;
    }
    console.log("showVisible "+i);
}

function filterKaffee() {
  var input, filter, table, div, name, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("container");
  div = table.getElementsByTagName("div");
  for (i = 0; i < div.length; i++) {
    name = div[i].getElementsByClassName("kritzelkaffee-table-name")[0];
    if (name) {
      txtValue = name.textContent || name.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        div[i].style.display = "";
      } else {
        div[i].style.display = "none";
      }
    }
  }
  showVisible();
}

window.addEventListener('scroll', showVisible);
showVisible();
</script>

</body>
</html>
"""
