<?php
    require_once "config/database.php";
    
    // Initialize message variable to avoid "Undefined variable" error
    $msg = "";

    // TEST CASE 0: Ensure logic only runs on Form Submit
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        
        $db = new Database();
        $conn = $db->connect();

        // Sanitize inputs
        $name = trim($_POST['name']);
        $email = trim($_POST['email']);
        $password = $_POST['password'];

        // TEST CASE 1: Check for Empty Fields
        if (empty($name) || empty($email) || empty($password)) {
            $msg = "Error: All fields are required.";
        } 
        // TEST CASE 2: Validate Email Format
        elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $msg = "Error: Invalid email format.";
        }
        // TEST CASE 3: Password Strength (e.g., min 6 characters)
        elseif (strlen($password) < 6) {
            $msg = "Error: Password must be at least 6 characters long.";
        }
        else {
            // TEST CASE 4: Check if Email Already Exists
            $checkStmt = $conn->prepare("SELECT email FROM users WHERE email = ?");
            $checkStmt->bind_param("s", $email);
            $checkStmt->execute();
            $checkStmt->store_result();

            if ($checkStmt->num_rows > 0) {
                $msg = "Error: This email is already registered.";
            } else {
                // Happy Path: Insert User
                $hashed = password_hash($password, PASSWORD_DEFAULT);
                $stmt = $conn->prepare("INSERT INTO users (name, email, password) VALUES (?, ?, ?)");
                $stmt->bind_param("sss", $name, $email, $hashed);

                if ($stmt->execute()) {
                    // Redirect only after successful insertion
                    header("Location: login.php?signup=success");
                    exit;
                } else {
                    $msg = "Database Error: " . $stmt->error;
                }
                $stmt->close();
            }
            $checkStmt->close();
        }
    }
?>

<!DOCTYPE html>
<html>
<head>
    <title>Sign Up</title>
</head>
<body>
    <h2>Sign Up</h2>
    <?php if (!empty($msg)): ?>
        <p style="color: red;"><?php echo $msg; ?></p>
    <?php endif; ?>

    <form method="POST" action="">
        <input type="text" name="name" placeholder="Name" value="<?php echo isset($_POST['name']) ? htmlspecialchars($_POST['name']) : ''; ?>" required><br><br>
        <input type="email" name="email" placeholder="Email" value="<?php echo isset($_POST['email']) ? htmlspecialchars($_POST['email']) : ''; ?>" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Sign Up</button>
        <br><br>
        <a href="login.php">Already have an account? LOGIN</a>
    </form>
</body>
</html>