<?php
require "db.php";

$name = $_POST['name'];
$email = $_POST['email'];
$password = password_hash($_POST['password'], PASSWORD_DEFAULT);

$stmt = $conn->prepare(
  "INSERT INTO users (name, email, password, auth_provider)
   VALUES (?, ?, ?, 'email')"
);
$stmt->bind_param("sss", $name, $email, $password);

if ($stmt->execute()) {
    echo "Signup successful";
} else {
    echo "Email already exists";
}
?>

<?php
session_start();
if (!isset($_SESSION['user_id']) && !isset($_SESSION['email'])) {
    header("Location: auth.html");
}
?>

