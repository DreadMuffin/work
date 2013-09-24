<html>

<body>
<form action="/cgi-bin/foo.pl" name="bleh">
<input type=submit>
</form>

<center><h1>Protocol search</h1>
<P>
<table border=1><tr><th>Protocolname</th><th>PETscanner</th>
                    <th>Bodysize</th><th>PDF-link</th></tr>
Scanner
<form method="POST" action="pdf.php">
<select name="search[]">
<option value="">Any</option>
<option value="PET3">PET 3</option>
<option value="PET4">PET 4</option>
<option value="PET5">PET 5</option>
<option value="PET6">PET 6</option>
</select>
Searchterm
<input type=text name=search[] size=15>
<input type=submit value"Send info">
</form>
</center>


<BR>

<?php 
$db = new PDO('mysql:host=127.0.0.1;dbname=protokoller','root','mysql');
$pdf = "pdf/";
$array = ($_POST["search"]);
$search=$array[1];
$scanner=$array[0];
foreach($db->query("select Protocolname, PETscanner, Bodysize from Protocols 
    where lower(Protocolname) like lower('%$search%') and PETscanner like 
    ('%$scanner%') order by PETscanner,Protocolname") as $row) {
    $downloadlink = $row[0] . "_" . $row[1] . ".pdf";
    print "<tr><td>" . $row[0] . "</td><td>" . $row[1] . "</td><td>" . $row[2] .
        "</td><td>" . "<a href=" . $pdf . $downloadlink .
        ">Download</a>" . "</td></tr>";
}
?>

</table>

</body>
</html>
