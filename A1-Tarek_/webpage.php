<?php
if (isset($_POST['submit'])){
	$results = '<br />Your first name is'.$_POST['firstname'];
	$results .= '<br /> Your last name is'.$_POST['lastname'];
} else{
	$results='You have not submitted anything';
}
?>
<html>
<head>
<meta http-equiv="Content-Type" content = "text/html: charset=utf-8" />
<title>
cURL
</title>
</head>
<body>
<?php echo $results; ?>
<form method ="POST" action="webpage.php">
<label> First Name: </label>
<input name="firstname" type="text" />
<label> Last Name: </label>
<input name="lastname" type="text" />
<br/>
<br/>
<input name="submit" type="submit" value="submit"/>
</form>
</body>
</html>