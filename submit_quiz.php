<?php

$answers = $_POST['answers'] ?? [];

$url = "http://127.0.0.1:5000/quiz/submit";

$data = [
    "answers" => $answers
];

$options = [
    "http" => [
        "header"  => "Content-Type: application/json\r\n",
        "method"  => "POST",
        "content" => json_encode($data)
    ]
];

$context  = stream_context_create($options);
$response = file_get_contents($url, false, $context);

$result = json_decode($response, true);

?>
<!DOCTYPE html>
<html>
<body>

<h2>Quiz Result</h2>

<p>
Score : <?php echo $result['score']; ?> / <?php echo $result['total']; ?>
</p>

<h3>Performance by language</h3>

<ul>
<?php foreach ($result['per_language_correct'] as $lang => $cnt): ?>
    <li><?php echo $lang; ?> : <?php echo $cnt; ?></li>
<?php endforeach; ?>
</ul>

</body>
</html>
