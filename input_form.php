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
        <label>Enter Job description</label>
        <input name="jd" type="text">
        <label>Upload resume</label>
        <input name="resume" type="file">
        <label>Enter mentor's comments</label>
        <input name="comments" type="text">
        <label>Enter git username</label>
        <input name="git" type="text">
        <button type="submit">Submit</button>
    </form>
</body>
</html>