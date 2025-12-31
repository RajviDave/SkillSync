<?php
    include("connection.php");
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - SkillSync</title>
    
</head>
<body>

    <form action="<?php $_SERVER['PHP_SELF']?>"  method="post">
        <label>Username:</label><br>
        <input type="text" name="username"><br>
        <label>Password:</label><br>
        <input type="password" name="password"><br>
        <input type="submit" name="submit">
    </form>

</body>
</html>

<?php

    if(isset($_POST["submit"])){
        $username = mysqli_real_escape_string($conn, $_POST["username"]);
        $password = mysqli_real_escape_string($conn, $_POST["password"]);
        
        $sql = "INSERT INTO signup(username,password) VALUES ('$username','$password')";
        
        if(mysqli_query($conn, $sql)){
            echo "user is registered";
        }
        else{
            echo "could not register user: " . mysqli_error($conn);
        }
    }
?>