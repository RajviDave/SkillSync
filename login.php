<!DOCTYPE HTML>  
<html>
<head>
<style>
.error {color: #FF0000;}
</style>
</head>
<body> 
    <div>
        <form action="login.php" method="post">
            <input type="text" name="email" value="Username"><br>
            <input type="text" name="password" value="password"><br>
            <input type="submit" name="submit" value="SUBMIT">
        </form>
    </div>
</body>
<?php
    if($_SERVER["REQUEST_METHOD"]=="POST"){
        echo "You are logged in";
    }
?>