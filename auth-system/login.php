<?php
require_once "config/Database.php";
require_once "classes/User.php";

$db = new Database();
$conn = $db->connect();

$user = new User($conn);

$msg = "";

if($_SERVER["REQUEST_METHOD"] == "POST"){

    $email = $_POST['email'];
    $password = $_POST['password'];

    if($user->login($email, $password)){
        $msg = "Login successful";
    }else{
        $msg = "Invalid email or password";
    }
}
?>

<form method="POST">
    <input type="email" name="email" placeholder="Email" required><br>
    <input type="password" name="password" placeholder="Password" required><br>
    <button type="submit">Login</button>
</form>

<p><?php echo $msg; ?></p>
