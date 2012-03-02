<html>
<head>
<title>Dicne</title>
</head>
<body>

<!-- list all series - equip with checkbuttons -->

<!-- after this small routine, $perl_output consists of id, name, series, path -->

<?php
$output = shell_exec('./indexing.pl');
$perl_output = explode("|",$output);
?>

<FORM METHOD=POST ACTION="mycgi.pl">

Følgende serier er klar til konvertering<br><br>

<!-- create the table, scanning through $perl_output -->

<table border="1">
<tr>
<td><b>Konverter</b></td>
<td><b>CPR</b></td>
<td><b>Navn</b></td>
<td><b>Serie</b></td>
<td><b>Resample</b></td>
</tr>
<tr>

<?php

for ($i = 0; $i < sizeof($perl_output)-2; $i++) {
	echo '<td><center><input type="checkbox" name="check" value="' . $i/4 . '"></center></td>';
	echo '<td>'; print "$perl_output[$i]"; echo '</td>';
	$i++;
	echo '<td>'; print "$perl_output[$i]"; echo '</td>';
	$i++;
	// post series as hidden
	echo '<input type="hidden" name="series" value="' . $perl_output[$i] . '">';
	echo '<td>'; print "$perl_output[$i]"; echo '</td>';
	$i++;
	// post path as hidden
	echo '<input type="hidden" name="path" value="' . $perl_output[$i] . '">';
	echo '<td><center><input type="checkbox" name="resample" value="' . ($i-3)/4 . '"></center></td>';
	echo '</tr><tr>';
}

?>

</tr>
</table>

<br><INPUT TYPE=SUBMIT NAME='ok'>


</form>

</body>
