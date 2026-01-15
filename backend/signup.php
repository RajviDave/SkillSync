<?php
header('Content-Type: application/json');
require "db.php";

$name = $_POST['name'] ?? '';
$email = $_POST['email'] ?? '';
$password = $_POST['password'] ?? '';

if (empty($name) || empty($email) || empty($password)) {
    echo json_encode(["status" => "error", "message" => "All fields are required"]);
    exit;
}

// Check if email already exists
$check = $conn->prepare("SELECT id FROM users WHERE email=?");
$check->bind_param("s", $email);
$check->execute();
$result = $check->get_result();

if ($result->num_rows > 0) {
    echo json_encode(["status" => "error", "message" => "Email already exists"]);
    exit;
}

$hashed_password = password_hash($password, PASSWORD_DEFAULT);

$stmt = $conn->prepare(
  "INSERT INTO users (name, email, password, auth_provider)
   VALUES (?, ?, ?, 'email')"
);
$stmt->bind_param("sss", $name, $email, $hashed_password);

if ($stmt->execute()) {
    session_start();
    $_SESSION['user_id'] = $stmt->insert_id;
    $_SESSION['email'] = $email;
    $_SESSION['name'] = $name;
    echo json_encode([
        "status" => "success", 
        "message" => "Signup successful",
        "user" => [
            "id" => $stmt->insert_id,
            "email" => $email,
            "name" => $name
        ]
    ]);
} else {
    echo json_encode(["status" => "error", "message" => "Signup failed. Please try again."]);
}
?>

