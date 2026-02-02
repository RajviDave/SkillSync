<?php

class User {

    private $conn;

    public function __construct($db){
        $this->conn = $db;
    }

    public function register($name, $email, $password){

        $hash = password_hash($password, PASSWORD_DEFAULT);

        $stmt = $this->conn->prepare(
            "INSERT INTO users (name,email,password) VALUES (?,?,?)"
        );

        $stmt->bind_param("sss", $name, $email, $hash);

        return $stmt->execute();
    }

    public function login($email, $password){

    $stmt = $this->conn->prepare(
        "SELECT id, password FROM users WHERE email=?"
    );

    $stmt->bind_param("s", $email);
    $stmt->execute();

    $result = $stmt->get_result();

    if($result->num_rows == 1){

        $row = $result->fetch_assoc();

        if(password_verify($password, $row['password'])){
            return true;
        }
    }

    return false;
}

}
