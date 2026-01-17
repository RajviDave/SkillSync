<?php
// Test database connection and table structure
header('Content-Type: text/html; charset=utf-8');

$host = "localhost";
$user = "root";
$pass = "";
$db   = "businessdb";

echo "<h2>Database Connection Test</h2>";

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    die("<p style='color:red;'>❌ Database connection failed: " . $conn->connect_error . "</p>");
}

echo "<p style='color:green;'>✅ Database connection successful!</p>";

// Check if 'user' table exists
$result = $conn->query("SHOW TABLES LIKE 'user'");
if ($result->num_rows > 0) {
    echo "<p style='color:green;'>✅ Table 'user' exists!</p>";
    
    // Show table structure
    echo "<h3>Table Structure:</h3>";
    $columns = $conn->query("DESCRIBE user");
    echo "<table border='1' cellpadding='5' style='border-collapse: collapse;'>";
    echo "<tr><th>Field</th><th>Type</th><th>Null</th><th>Key</th><th>Default</th><th>Extra</th></tr>";
    while ($row = $columns->fetch_assoc()) {
        echo "<tr>";
        echo "<td>" . htmlspecialchars($row['Field']) . "</td>";
        echo "<td>" . htmlspecialchars($row['Type']) . "</td>";
        echo "<td>" . htmlspecialchars($row['Null']) . "</td>";
        echo "<td>" . htmlspecialchars($row['Key']) . "</td>";
        echo "<td>" . htmlspecialchars($row['Default'] ?? 'NULL') . "</td>";
        echo "<td>" . htmlspecialchars($row['Extra']) . "</td>";
        echo "</tr>";
    }
    echo "</table>";
    
    // Count records
    $count = $conn->query("SELECT COUNT(*) as count FROM user");
    $row = $count->fetch_assoc();
    echo "<p>Total users in database: <strong>" . $row['count'] . "</strong></p>";
    
} else {
    echo "<p style='color:red;'>❌ Table 'user' does NOT exist!</p>";
    echo "<p>Please create the table with the following structure:</p>";
    echo "<pre style='background:#f5f5f5; padding:10px; border:1px solid #ddd;'>";
    echo "CREATE TABLE IF NOT EXISTS `user` (\n";
    echo "  `id` int(11) NOT NULL AUTO_INCREMENT,\n";
    echo "  `name` varchar(255) NOT NULL,\n";
    echo "  `email` varchar(255) NOT NULL UNIQUE,\n";
    echo "  `password` varchar(255) DEFAULT NULL,\n";
    echo "  `google_id` varchar(255) DEFAULT NULL,\n";
    echo "  `auth_provider` enum('email','google') DEFAULT 'email',\n";
    echo "  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,\n";
    echo "  PRIMARY KEY (`id`),\n";
    echo "  UNIQUE KEY `email` (`email`)\n";
    echo ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;";
    echo "</pre>";
}

// Check if 'users' table exists (old name)
$result2 = $conn->query("SHOW TABLES LIKE 'users'");
if ($result2->num_rows > 0) {
    echo "<p style='color:orange;'>⚠️ Table 'users' (plural) also exists. You may need to rename it to 'user' (singular) or update the code.</p>";
}

$conn->close();
?>
