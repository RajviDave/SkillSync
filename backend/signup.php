<?php
// CORS headers
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Enable error logging
error_reporting(E_ALL);
ini_set('display_errors', 0);
ini_set('log_errors', 1);

require "db.php";

try {
    $name = $_POST['name'] ?? '';
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';

    if (empty($name) || empty($email) || empty($password)) {
        http_response_code(400);
        echo json_encode(["status" => "error", "message" => "All fields are required"]);
        exit;
    }

    // Validate email format
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        echo json_encode(["status" => "error", "message" => "Invalid email format"]);
        exit;
    }

    // Check if email already exists - using 'user' table (singular)
    $check = $conn->prepare("SELECT id FROM user WHERE email=?");
    if (!$check) {
        throw new Exception("Prepare failed: " . $conn->error);
    }
    
    $check->bind_param("s", $email);
    if (!$check->execute()) {
        throw new Exception("Execute failed: " . $check->error);
    }
    
    $result = $check->get_result();

    if ($result->num_rows > 0) {
        http_response_code(409);
        echo json_encode(["status" => "error", "message" => "Email already exists"]);
        exit;
    }

    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    // Using 'user' table (singular) as per database
    $stmt = $conn->prepare(
      "INSERT INTO user (name, email, password, auth_provider)
       VALUES (?, ?, ?, 'email')"
    );
    
    if (!$stmt) {
        throw new Exception("Prepare failed: " . $conn->error);
    }
    
    $stmt->bind_param("sss", $name, $email, $hashed_password);

    if ($stmt->execute()) {
        session_start();
        $_SESSION['user_id'] = $stmt->insert_id;
        $_SESSION['email'] = $email;
        $_SESSION['name'] = $name;
        
        http_response_code(200);
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
        throw new Exception("Execute failed: " . $stmt->error);
    }
    
    $stmt->close();
    $check->close();
    
} catch (Exception $e) {
    error_log("Signup error: " . $e->getMessage());
    http_response_code(500);
    echo json_encode([
        "status" => "error", 
        "message" => "Signup failed. Please try again.",
        "debug" => (ini_get('display_errors') ? $e->getMessage() : null)
    ]);
} finally {
    if (isset($conn)) {
        $conn->close();
    }
}
?>

