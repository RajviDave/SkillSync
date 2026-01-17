<?php
// Enable error reporting for debugging (disable in production)
error_reporting(E_ALL);
ini_set('display_errors', 0); // Don't display errors to users, but log them

$host = "localhost";
$user = "root";
$pass = "";
$db   = "businessdb";

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    error_log("Database connection failed: " . $conn->connect_error);
    die(json_encode(["error" => "Database connection failed"]));
}

// Set charset to utf8
$conn->set_charset("utf8");
?>