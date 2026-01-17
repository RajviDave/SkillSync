<?php
// CORS headers
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Access-Control-Allow-Credentials: true');

// Handle preflight request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

session_start();

if (isset($_SESSION['user_id']) && isset($_SESSION['email'])) {
    http_response_code(200);
    echo json_encode([
        "authenticated" => true,
        "user" => [
            "id" => $_SESSION['user_id'],
            "email" => $_SESSION['email'],
            "name" => $_SESSION['name'] ?? 'User'
        ]
    ]);
} else {
    http_response_code(200);
    echo json_encode(["authenticated" => false]);
}
?>
