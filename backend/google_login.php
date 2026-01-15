<?php
header('Content-Type: application/json');
require "db.php";

$token = $_POST['token'] ?? '';

if (empty($token)) {
    echo json_encode(["status" => "error", "message" => "Token is required"]);
    exit;
}

$googleData = json_decode(
  file_get_contents(
    "https://oauth2.googleapis.com/tokeninfo?id_token=".$token
  ),
  true
);

if (!$googleData || isset($googleData['error'])) {
    echo json_encode(["status" => "error", "message" => "Invalid Google token"]);
    exit;
}

$email = $googleData['email'] ?? '';
$name  = $googleData['name'] ?? 'User';
$google_id = $googleData['sub'] ?? '';

if (empty($email)) {
    echo json_encode(["status" => "error", "message" => "Could not retrieve email from Google"]);
    exit;
}

$stmt = $conn->prepare("SELECT id, name FROM users WHERE email=?");
$stmt->bind_param("s", $email);
$stmt->execute();
$result = $stmt->get_result();

$user_id = null;
if ($result->num_rows == 0) {
    // New user - insert
    $insert = $conn->prepare(
      "INSERT INTO users (name,email,google_id,auth_provider)
       VALUES (?,?,?,'google')"
    );
    $insert->bind_param("sss", $name, $email, $google_id);
    if ($insert->execute()) {
        $user_id = $insert->insert_id;
    }
} else {
    // Existing user
    $user = $result->fetch_assoc();
    $user_id = $user['id'];
    $name = $user['name'] ?? $name;
}

session_start();
$_SESSION['user_id'] = $user_id;
$_SESSION['email'] = $email;
$_SESSION['name'] = $name;

echo json_encode([
    "status" => "success", 
    "message" => "Google login successful",
    "user" => [
        "id" => $user_id,
        "email" => $email,
        "name" => $name
    ]
]);
?>
