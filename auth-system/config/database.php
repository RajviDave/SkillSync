<?php

class Database {
    private $host = "localhost";
    private $db   = "auth_system";
    private $user = "root";
    private $pass = "";

    public $conn;

    public function connect() {
        $this->conn = new mysqli(
            $this->host,
            $this->user,
            $this->pass,
            $this->db
        );

        if ($this->conn->connect_error) {
            die("DB Error");
        }

        return $this->conn;
    }
}
