<?php
$host = "localhost";
$user = "root";
$pass = "";
$db   = "businessdb";

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    die("Database connection failed");
}
?>
