<?php
require_once "config/Database.php";
require_once "classes/User.php";

$db = new Database();
$conn = $db->connect();

$user = new User($conn);

$msg = "";

if($_SERVER["REQUEST_METHOD"] == "POST"){

    $name = $_POST['name'];
    $email = $_POST['email'];
    $password = $_POST['password'];

    if($user->register($name,$email,$password)){
        $msg = "Registered successfully";
    }else{
        $msg = "Registration failed";
    }
}
?>

<form method="POST">
    <input type="text" name="name" placeholder="Name" required><br>
    <input type="email" name="email" placeholder="Email" required><br>
    <input type="password" name="password" placeholder="Password" required><br>
    <button type="submit">Sign Up</button>
    <a href="login.php">LOGIN</a>
</form>

<p><?php echo $msg; ?></p>
