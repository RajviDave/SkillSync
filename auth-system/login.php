<?php
session_start();
require_once "config/database.php";

$error = "";

// TEST CASE 0: Ensure logic only runs on Form Submit
if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $db = new Database();
    $conn = $db->connect();

    // Sanitize inputs
    $email = trim($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';

    // TEST CASE 1: Check for Empty Fields
    if (empty($email) || empty($password)) {
        $error = "Please fill in both email and password.";
    } else {
        // Prepare statement to find user
        $stmt = $conn->prepare("SELECT id, name, password FROM users WHERE email = ?");
        $stmt->bind_param("s", $email);
        $stmt->execute();
        $result = $stmt->get_result();

        // TEST CASE 2: User Exists Check
        if ($result->num_rows === 1) {
            $row = $result->fetch_assoc();

            // TEST CASE 3: Password Verification
            if (password_verify($password, $row['password'])) {
                // Success: Set session variables
                $_SESSION['user_id']   = $row['id'];
                $_SESSION['user_name'] = $row['name'];

                // Redirect to the dashboard/input form
                header("Location: ../templates/input_form.html");
                exit;
            } else {
                // Failed Test Case 3
                $error = "Incorrect password.";
            }
        } else {
            // Failed Test Case 2 (Email not found)
            $error = "No account found with that email.";
        }
        $stmt->close();
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    
    <?php if(!empty($error)): ?>
        <p style='color:red; font-weight:bold;'><?php echo $error; ?></p>
    <?php endif; ?>

    <?php if(isset($_GET['signup']) && $_GET['signup'] == 'success'): ?>
        <p style='color:green;'>Signup successful! Please login.</p>
    <?php endif; ?>

    <form method="POST" action="login.php">
        <input type="email" name="email" placeholder="Email" required value="<?php echo isset($_POST['email']) ? htmlspecialchars($_POST['email']) : ''; ?>"><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Login</button>
        <br><br>
        <a href="signup.php">Don't have an account? Sign Up</a>
    </form>
</body>
</html>