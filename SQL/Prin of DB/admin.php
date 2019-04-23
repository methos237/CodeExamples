<?php

/**
 * admin.php
 *
 * Last Updated: 4/10/2019
 *
 * Description: Form for addition of books into requisite tables in the 471books database
 * CSC 471 HW 7 / Dr. Fred Sadri / UNCG / Spring 2019
 *
 * @author James Knox Polk <jkpolk@uncg.edu>
 */


require_once ('DBConnect.php');

$db = DBConnect::instance ();
$genre_list = $db->getAll ("SELECT * FROM genres");
$isbn = $title = $all_authors = $genre = $pub_name = $pub_city = $pub_country = $pub_year = $price = $authors_arr = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $isbn = test_input($_POST["isbn"]);
    $title = test_input($_POST["title"]);
    $all_authors = test_input($_POST["authors"]);
    $genre = test_input($_POST["genre"]);
    $pub_name = test_input($_POST["publisher_name"]);
    $pub_city = test_input($_POST["publisher_city"]);
    $pub_country = test_input($_POST["publisher_country"]);
    $pub_year = test_input($_POST["year"]);
    $price = test_input($_POST["price"]);

    $db->run ("INSERT into book (ISBN, genre_id, year, title, price) VALUES ($isbn,$genre,$pub_year,'$title',$price)");

    // Publisher Handling
    $pubs = $db->getOne ("SELECT * from publishers WHERE publisher_name = '$pub_name' AND city = '$pub_city' AND country = '$pub_country'");
    $pub_id = $pubs['publisher_id'];
    if (!$pub_id) {
        $db->run ("INSERT into publishers (publisher_name, city, country) VALUES ('$pub_name', '$pub_city', '$pub_country')");
        $pubs = $db->getOne ("SELECT * from publishers WHERE publisher_name = '$pub_name' AND city = '$pub_city' AND country = '$pub_country'");
        $pub_id = $pubs['publisher_id'];
    }
    $db->run ("UPDATE book SET publisher_id='$pub_id' WHERE ISBN = $isbn");


    // Author Handling
    $authors_arr = preg_split ('/\n/', $all_authors);
    foreach ($authors_arr as $authors) {
        $authors = explode (",", $authors);
        $auths = $db->getOne ("SELECT * FROM authors WHERE last_name = '$authors[0]' AND first_name = '$authors[1]'");
        $author_id = $auths['author_id'];
        if (!$author_id) {
            $db->run ("INSERT into authors (last_name, first_name) VALUES ('$authors[0]', '$authors[1]')");
            $auths = $db->getOne ("SELECT * FROM authors WHERE last_name = '$authors[0]' AND first_name = '$authors[1]'");
            $author_id = $auths['author_id'];
        }
        $db->run ("INSERT into book_authors (book_ISBN, author_author_id) VALUES ('$isbn', '$author_id')");
    }
}

function test_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}
?>

<!DOCTYPE html>
<html lang="en">
    <head>
        <title>CSC 471 HW 3 / Dr. Fred Sadri / UNCG</title>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    </head>
    <body>
        <h2><a href="index.php">Return to Index</a></h2>
        <form class="w3-container"  method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
            <div class="w3-container">
                <h2>Add A Book</h2>
            </div>
            <br>
            <label for="isbn">ISBN-13 </label>
                <input id="isbn" name="isbn" class="w3-input w3-border" style="width:30%" type="text" maxlength="255" value=""/>
            <br>
            <label for="title">Book Title </label>
                <input id="title" name="title" class="w3-input w3-border " style="width:30%" type="text" maxlength="255" value=""/>
            <br>
            <label for="authors">Authors (Add each author on a new line; Last Name, First Name) </label>
                <textarea id="authors" name="authors" class="w3-input w3-border " style="width:30%"></textarea>
            <br>
            <label for="genre">Genre</label><br>
                <select class="w3-select w3-border" style="width:30%" id="genre" name="genre">
                    <option value="" selected="selected">Select...</option>
                    <?php
                    foreach ($genre_list as $item)
                        echo "<option value=".$item['genre_id'].">".$item['genre_name']."</option>"
                    ?>
                </select>

            <br><br>
            <label for="publisher_name">Publisher Name </label>
                <input id="publisher_name" name="publisher_name" class="w3-input w3-border " style="width:30%" type="text" maxlength="255" value=""/>
            <br>
            <label for="publisher_city">Publisher City </label>
                <input id="publisher_city" name="publisher_city" class="w3-input w3-border " style="width:30%" type="text" maxlength="255" value=""/>
            <br>
            <label for="publisher_country">Publisher Country </label>
                <input id="publisher_country" name="publisher_country" class="w3-input w3-border " style="width:30%" type="text" maxlength="255" value=""/>
            <br>
            <label for="year">Published Year </label>
                <input id="year" name="year" class="w3-input w3-border " style="width:30%" type="text" maxlength="255" value=""/>
            <br>
            <label for="price">Price </label><br>
            $ <input id="price" name="price" class="w3-input w3-border" size="10" style="width:30%" value="" type="text" />
            <br><br>
            <input class="w3-btn w3-grey w3-round" type="submit" name="submit" value="Submit" />
        </form>
    <br><br><br><br>


        <?php
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            echo "<h2>Your Input:</h2>";
            echo "ISBN: \t" . $isbn;
            echo "<br>";
            echo "Title: \t" . $title;
            echo "<br>";
            echo "Authors: ";
            foreach ( $authors_arr as $authors ) {
                echo "\t\t" . $authors;
            }
            echo "<br>";
            echo "Genre: \t" . $genre;
            echo "<br>";
            echo "Publisher Name: " . $pub_name;
            echo "<br>";
            echo "Publisher City: " . $pub_city;
            echo "<br>";
            echo "Publisher Country: " . $pub_country;
            echo "<br>";
            echo "Published year: " . $pub_year;
            echo "<br>";
            echo "Price:\t\t $" . $price;
        }
        ?>
    </body>
</html>
