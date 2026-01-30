
<!DOCTYPE HTML>  
<html>
<head>
<style>
.error {color: #FF0000;}
</style>
</head>
<body> 

<?php
    $username=$email=$passwd="";
    $usernamERR=$emailERR=$passwdERR="";

    if($_SERVER["REQUEST_METHOD"]=="POST"){
        if (empty($_POST["name"])){
            $usernameERR="username is requirement";
        }
    }

    
?>