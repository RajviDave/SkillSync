<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Input Form</title>
</head>
<body>
    <h1>Input Form</h1>
    <form method="POST" action="input_form.php">
        <label>Enter Job description</label><br>
        <input name="jd" type="text"><br>
        <label>Upload resume</label><br>
        <input name="resume" type="file"><br>
        <label>Enter mentor's comments</label><br>
        <input name="comments" type="text"><br>
        <label>Enter git username</label><br>
        <input name="git" type="text"><br>
        <button type="submit">Submit</button><br>
    </form>
</body>
</html>

<?php


?>