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
    $token = $_POST['token'] ?? '';

    if (empty($token)) {
        http_response_code(400);
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
        http_response_code(401);
        echo json_encode(["status" => "error", "message" => "Invalid Google token"]);
        exit;
    }

    $email = $googleData['email'] ?? '';
    $name  = $googleData['name'] ?? 'User';
    $google_id = $googleData['sub'] ?? '';

    if (empty($email)) {
        http_response_code(400);
        echo json_encode(["status" => "error", "message" => "Could not retrieve email from Google"]);
        exit;
    }

    // Using 'user' table (singular) as per database
    $stmt = $conn->prepare("SELECT id, name FROM user WHERE email=?");
    
    if (!$stmt) {
        throw new Exception("Prepare failed: " . $conn->error);
    }
    
    $stmt->bind_param("s", $email);
    
    if (!$stmt->execute()) {
        throw new Exception("Execute failed: " . $stmt->error);
    }
    
    $result = $stmt->get_result();

    $user_id = null;
    if ($result->num_rows == 0) {
        // New user - insert
        $insert = $conn->prepare(
          "INSERT INTO user (name,email,google_id,auth_provider)
           VALUES (?,?,?,'google')"
        );
        
        if (!$insert) {
            throw new Exception("Prepare failed: " . $conn->error);
        }
        
        $insert->bind_param("sss", $name, $email, $google_id);
        
        if ($insert->execute()) {
            $user_id = $insert->insert_id;
        } else {
            throw new Exception("Insert failed: " . $insert->error);
        }
        
        $insert->close();
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

    http_response_code(200);
    echo json_encode([
        "status" => "success", 
        "message" => "Google login successful",
        "user" => [
            "id" => $user_id,
            "email" => $email,
            "name" => $name
        ]
    ]);
    
    $stmt->close();
    
} catch (Exception $e) {
    error_log("Google login error: " . $e->getMessage());
    http_response_code(500);
    echo json_encode([
        "status" => "error", 
        "message" => "Google login failed. Please try again.",
        "debug" => (ini_get('display_errors') ? $e->getMessage() : null)
    ]);
} finally {
    if (isset($conn)) {
        $conn->close();
    }
}
?>
