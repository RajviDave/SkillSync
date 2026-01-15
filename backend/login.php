<?php
require "db.php";

$email = $_POST['email'];
$password = $_POST['password'];

$stmt = $conn->prepare(
  "SELECT * FROM users WHERE email=? AND auth_provider='email'"
);
$stmt->bind_param("s", $email);
$stmt->execute();

$result = $stmt->get_result();
$user = $result->fetch_assoc();

if ($user && password_verify($password, $user['password'])) {
    session_start();
    $_SESSION['user_id'] = $user['id'];
    echo "Login successful";
} else {
    echo "Invalid credentials";
}
?>

<?php
session_start();
if (!isset($_SESSION['user_id']) && !isset($_SESSION['email'])) {
    header("Location: auth.html");
}
?>
