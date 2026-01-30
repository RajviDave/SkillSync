
<!DOCTYPE HTML>  
<html>
<head>
<style>
.error {color: #FF0000;}
</style>
</head>
<body> 

    <form action="index.php" method="post">
    <input type="text" name="username" value="rajvidave"><br>
    <input type="text" name="email" value="Email"><br>
    <input type="password" name="passwd" value="Passwd"><br>
    <input type="submit" name="submit" value="submit">
    </form>
</body>

<?php
if($_SERVER["REQUEST_METHOD"]=="POST"){
    $username=$_POST["username"];
    $email=$_POST["email"];
    $passwd=$_POST["passwd"];
    $usernameERR=$emailERR=$passwdERR=" ";
    $usernamecharERR=$emailcharERR=$passcharERR=" ";
    

    if($_SERVER["REQUEST_METHOD"]=="POST"){
        if (empty($_POST["username"])){
            $usernameERR="username is requirement";
        }elseif(!preg_match('/^[A-Za-z0-9]+$/',$username)){
            $usernamecharERR="Only characters and numbers are allowed";
        }

        if(empty($_POST["email"])){
            $emailERR="Email is required";
        }elseif(!filter_var($email, FILTER_VALIDATE_EMAIL)){
            $emailcharERR="Enter correct email address";
        }

        if(empty($_POST["passwd"])){
            $passwdERR="Enter password";
        }elseif((strlen($_POST["passwd"]))<8){
            $passcharERR="Enter 8 character long password";
        }
            
        }

        echo $username;
}
?>