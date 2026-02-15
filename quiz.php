<?php

$url = "http://127.0.0.1:5000/quiz/generate";

$data = [
    "languages" => ["python","sql"],
    "total_questions" => 6
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

$questions = json_decode($response, true);   // <<< use this

echo "<pre>";
print_r($questions);
echo "</pre>";
die();

?>
<!DOCTYPE html>
<html>
<body>

<form method="post" action="submit_quiz.php">

<?php foreach ($questions as $q): ?>

    <p><b><?php echo $q['question']; ?></b></p>

    <label>
        <input type="radio" name="answers[<?php echo $q['id']; ?>]" value="A">
        <?php echo $q['option_a']; ?>
    </label><br>

    <label>
        <input type="radio" name="answers[<?php echo $q['id']; ?>]" value="B">
        <?php echo $q['option_b']; ?>
    </label><br>

    <label>
        <input type="radio" name="answers[<?php echo $q['id']; ?>]" value="C">
        <?php echo $q['option_c']; ?>
    </label><br>

    <label>
        <input type="radio" name="answers[<?php echo $q['id']; ?>]" value="D">
        <?php echo $q['option_d']; ?>
    </label><br><br>

<?php endforeach; ?>

<button type="submit">Submit Quiz</button>

</form>

</body>
</html>
