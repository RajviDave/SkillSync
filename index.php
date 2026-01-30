<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up - SkillSync</title>
    <style> </style>
</head>
<body>
    <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" method="post">
        <input type="text" name="email" value="one@example.com"><br>
        <input type="text" name="username" value="User"><br>
        <input type="password" name="pass" value="1234"><br>
        <input type="submit" name="submit" value="submit">
    </form>
</body>
</html>

<?php 
    if(isset($_submit)){

        echo "done";
        // $email=$_POST["email"];
        // $username=$_POST["username"];
        // $pass=$_POST["pass"];

        // echo "$email";
    }
?>