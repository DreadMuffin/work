<html>
<head>
<title>Dicne</title>
</head>
<body>

<!-- list all series - equip with checkbuttons -->

<!-- after this small routine, $perl_output consists of id, name, series, p -->

<?php
$output = shell_exec('./index.pl');
$perl_output = explode("|",$output);
?>

<form method="post" action="mailto:mikkeloberg@gmail.com">

Følgende serier er klar til konvertering<br><br>

<!-- create the table, scanning through $perl_output -->

<table border="1">
<tr>
<td><b>Check</b></td>
<td><b>CPR</b></td>
<td><b>Navn</b></td>
<td><b>Serie</b></td>
</tr>
<tr>

<?php

for ($i = 0; $i < sizeof($perl_output)-2; $i++) {
	echo '<td><center><input type="checkbox" name="series" value="0"></center></td>';
	echo '<td>'; print "$perl_output[$i]"; echo '</td>';
	$i++;
	echo '<td>'; print "$perl_output[$i]"; echo '</td>';
	$i++;
	echo '<td>'; print "$perl_output[$i]"; echo '</td>';
	$i++;
	echo '</tr><tr>';
}
?>

</tr>
</table>

<br><input type="submit" value="Konverter">


</form>
