<html>
<head>
<title>Dicne</title>
</head>
<body>

<?php

// dicne.php 

// placeholder-associative arrays

$series = array("1.1.111.1.1.1111111111.1.111.111111111.1111", 
                "2.2.222.2.2.2222222222.2.222.222222222.2222", 
                "3.3.333.3.3.3333333333.3.333.333333333.3333"); 

$id = array("1.1.111.1.1.1111111111.1.111.111111111.1111" => "1234567890",
				"2.2.222.2.2.2222222222.2.222.222222222.2222" => "2345678901",
				"3.3.333.3.3.3333333333.3.333.333333333.3333" => "3456789012");
				
$name = array("1.1.111.1.1.1111111111.1.111.111111111.1111" => "Thomsen, Tim",
				"2.2.222.2.2.2222222222.2.222.222222222.2222" => "Thomsen, Tim",
				"3.3.333.3.3.3333333333.3.333.333333333.3333" => "Larsen, Lone");

?>

<!-- list all series - equip with checkbuttons -->

<form method="post" action="mailto:mikkeloberg@gmail.com">

Følgende serier er klar til konvertering<br><br>

<table border="1">
<tr><td></td></td><td>CPR</td><td>Navn</td><td>Serie</tr>
<tr><td><input type="checkbox" name="series" value="$series[0]"></td></td>
<td><?php echo $id{"$series[0]"} ?></td>
<td><?php echo $name{"$series[0]"} ?></td>
<td><?php echo $series[0] ?></tr>
<tr><td><input type="checkbox" name="series" value="$series[1]"></td></td>
<td><?php echo $id{"$series[1]"} ?></td>
<td><?php echo $name{"$series[1]"} ?></td>
<td><?php echo $series[1] ?></tr>
<tr><td><input type="checkbox" name="series" value="$series[2]"></td></td>
<td><?php echo $id{"$series[2]"} ?></td>
<td><?php echo $name{"$series[2]"} ?></td>
<td><?php echo $series[2] ?></tr>
</table>

<br><input type="submit" value="Konverter">


</form>
