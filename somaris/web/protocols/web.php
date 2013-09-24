<html>

<body>

<FORM METHOD="LINK" ACTION="pdf.php">
    <INPUT TYPE="submit" VALUE="Open protocol">
</FORM>

<FORM METHOD="LINK" ACTION="compare.php">
    <INPUT TYPE="submit" VALUE="Compare protocls">
</FORM>

<FORM METHOD="LINK" ACTION="advanced.php">
    <INPUT TYPE="submit" VALUE="Advanced settings">
</FORM>

<form action="web.php" method="post">
    <input type="submit" name="Update"/>
</form>

<?php
echo exec('ls');

?>






</body>

</html>
