<?php
require "db.php";

$token = $_POST['token'];

$googleData = json_decode(
  file_get_contents(
    "https://oauth2.googleapis.com/tokeninfo?id_token=".$token
  ),
  true
);

$email = $googleData['email'];
$name  = $googleData['name'];
$google_id = $googleData['sub'];

$stmt = $conn->prepare("SELECT id FROM users WHERE email=?");
$stmt->bind_param("s", $email);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows == 0) {
    $insert = $conn->prepare(
      "INSERT INTO users (name,email,google_id,auth_provider)
       VALUES (?,?,?,'google')"
    );
    $insert->bind_param("sss", $name, $email, $google_id);
    $insert->execute();
}

session_start();
$_SESSION['email'] = $email;

echo "Google login successful";
?>

<?php
session_start();
if (!isset($_SESSION['user_id']) && !isset($_SESSION['email'])) {
    header("Location: auth.html");
}
?>
