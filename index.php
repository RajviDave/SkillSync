
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
    $usernamecharERR=$emailcharERR="";

    if($_SERVER["REQUEST_METHOD"]=="POST"){
        if (empty($_POST["username"])){
            $usernameERR="username is requirement";
        }elseif(!preg_match(`/^[A-Za-z0-9]+$/`,$username)){
            $usernamecharERR="Only characters and numbers are allowed";
        }

        if(empty($_POST["email"])){
            $emailERR="Email is required";
        }elseif(!preg_match(`@`,$email)){
            $emailcharERR="Enter correct email address";
        }

        if(empty($_POST["password"])){
            $passWD="Enter password";
        }elseif((strlen($_POST["password"]))<8){
            echo "Enter 8 character long password";
        }
            
        }
?>
    <input type="text" name="email" value="<?php echo "$email";?>"><br>
    <input type="password" name="passwd" value="<?php echo "$passwd";?>"><br>
    <input type="text" name="username" value="<?php echo "$username";?>"><br>
    <input type="submit" name="submit" value="SUBMIT">
</body>