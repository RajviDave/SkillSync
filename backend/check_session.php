<?php
header('Content-Type: application/json');
session_start();

if (isset($_SESSION['user_id']) && isset($_SESSION['email'])) {
    echo json_encode([
        "authenticated" => true,
        "user" => [
            "id" => $_SESSION['user_id'],
            "email" => $_SESSION['email'],
            "name" => $_SESSION['name'] ?? 'User'
        ]
    ]);
} else {
    echo json_encode(["authenticated" => false]);
}
?>
