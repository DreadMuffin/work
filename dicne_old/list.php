<html>
<head>
<title>Dicne</title>
<!--<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">-->
</head>
<body bgcolor="F0E68C">

<!-- list all series - equip with checkbuttons -->

<?php

### init

$bgclrsw = 0;
$dumpnr = 5;
$output = shell_exec('./listing.pl');
$perl_output = explode("|",$output);

?>

<form method=post action="converting.pl">

<!-- create the table, scanning through $perl_output -->

<table bgcolor='white' align=center width=850>
<tr>
   	<td colspan='5'><br><center><img src=images/regh_scaled.png align=absmiddle></center><br><br>
</tr>

<tr><td colspan='5'><p>&nbsp;</p></tr>
<tr><td colspan='5'>Marker de serier du vil konvertere, ved at klikke i boksene til venstre.</tr>
<tr><td colspan='5'><p>&nbsp;</p></tr>

<!--

<tr><td colspan='5'>Vil du derudover resample en serie, så klik også i boksene til højre.</tr>
<tr><td colspan='5'><p>&nbsp;</p></tr>

-->

<tr>
<td><b></b></td>
<td><b>CPR</b></td>
<td><b>Navn</b></td>
<td><b>Dato | Tid</b></td>

<!-- Removal of resampling column

<td><b><center>Resample</center></b></td>

-->

</tr>

<?php

for ($i = 0; $i < sizeof($perl_output)-($dumpnr-1); $i++) {
	## small loop for switching line-color	
	if ($bgclrsw&1) {
		echo '<tr bgcolor="B0E0E6">'; } else {
		echo '<tr bgcolor="white">';
	}
	$bgclrsw++;
	echo '<td><center><input type="checkbox" name="check" value="' . $i/($dumpnr+1) . '"></center></td>';
	echo '<td>'; print "$perl_output[$i]"; echo '</td>';
	// post cpr as hidden
	echo '<input type="hidden" name="cpr" value="' . $perl_output[$i] . '">';
	$i++;
	echo '<td>'; print "$perl_output[$i]"; echo '</td>';
	$i++;
	// post series as hidden
	echo '<input type="hidden" name="series" value="' . $perl_output[$i] . '">';
	$i++;
	// post path as hidden
	echo '<input type="hidden" name="path" value="' . $perl_output[$i] . '">';
	$i++;
	// post date as hidden
	echo '<input type="hidden" name="date" value="' . $perl_output[$i] . '">';	
	echo '<td>'; print "$perl_output[$i] | ";
	$i++;
	// post time as hidden
	echo '<input type="hidden" name="time" value="' . $perl_output[$i] . '">';
	print "$perl_output[$i]"; echo '</td>';
	// post resample as hidden - all are "yes"
	echo '<td><center><input type="checkbox" checked="yes" style="display:none" name="resample" value="' . ($i-($dumpnr))/($dumpnr+1) . '"></center></td>';
	echo '</tr>';
}

?>

</tr>
<tr><td colspan='5'><p>&nbsp;</p></tr>
<tr><TH colspan='5'><input type='submit' value='Konverter' style='width:200;height:60;font-size:30;font-weight:bold'></tr>
<tr><td colspan='5'><p>&nbsp;</p></tr>
</table>

</form>

</body>
