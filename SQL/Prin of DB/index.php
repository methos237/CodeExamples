<?php

/**
 * index.php
 *
 * Last Updated: 4/10/2019
 *
 * Description: Displays table contents for 471books database
 * CSC 471 HW 7 / Dr. Fred Sadri / UNCG
 *
 * @author James Knox Polk <jkpolk@uncg.edu>
 */


require_once ('DBConnect.php');

$content = "Please click on a query to run";

$args = explode('=', rtrim($_SERVER['QUERY_STRING'], '/'));
$method = array_shift($args);

$db = DBConnect::instance ();
$book = $db->getAll ("SELECT * FROM book");
$genres = $db->getAll ("SELECT * FROM genres");
$publishers = $db->getAll ("SELECT * FROM publishers");
$authors = $db->getAll ("SELECT * FROM authors");
$book_authors = $db->getAll ("SELECT * FROM book_authors");

switch($method) {
    case 'query1':
        $content = "<table class='w3-table-all'>
                        <tr>
                            <th>ISBN</th>
                            <th>publisher_id</th>
                            <th>genre_id</th>
                            <th>year</th>
                            <th>title</th>
                            <th>price</th>
                        </tr>";
        foreach ($book as $data){
            $content .= "<tr><td>".$data['ISBN']."</td><td>".$data['publisher_id']."</td><td>".$data['genre_id']."</td><td>".$data['year']."</td><td>".$data['title']."</td><td>$".$data['price']."</td></tr>";
        }
        $content.="</table>";
        break;
    case 'query2':
        $content = "<table class='w3-table-all'>
                        <tr>
                            <th>genre_id</th>
                            <th>genre_name</th>
                        </tr>";
        foreach ($genres as $data){
            $content .= "<tr><td>".$data['genre_id']."</td><td>".$data['genre_name']."</td></tr>";
        }
        $content.="</table>";
        break;
    case 'query3':
        $content = "<table class='w3-table-all'>
                        <tr>
                            <th>publisher_id</th>
                            <th>publisher_name</th>
                            <th>city</th>
                            <th>country</th>
                        </tr>";
        foreach ($publishers as $data){
            $content .= "<tr><td>".$data['publisher_id']."</td><td>".$data['publisher_name']."</td><td>".$data['city']."</td><td>".$data['country']."</td></tr>";
        }
        $content.="</table>";
        break;
    case 'query4':
        $content = "<table class='w3-table-all'>
                        <tr>
                            <th>author_id</th>
                            <th>first_name</th>
                            <th>last_name</th>
                        </tr>";
        foreach ($authors as $data){
            $content .= "<tr><td>".$data['author_id']."</td><td>".$data['first_name']."</td><td>".$data['last_name']."</td></tr>";
        }
        $content.="</table>";
        break;
    case 'query5' :
        $content = "<table class='w3-table-all'>
                        <tr>
                            <th>book_ISBN</th>
                            <th>author_author_id</th>
                        </tr>";
        foreach ($book_authors as $data){
            $content .= "<tr><td>".$data['book_ISBN']."</td><td>".$data['author_author_id']."</td></tr>";
        }
        $content.="</table>";
        break;
    default:
        $content = "Please click on a query to run";
}

?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>CSC 471 HW 7 / Dr. Fred Sadri / UNCG</title>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    </head>
    <body>
    <h1><a href="index.php">CSC 471 HW 7 / Dr. Fred Sadri / UNCG</a></h1>
        <div>
            <h2><a href="admin.php">Insert a new book</a></h2>
            <p><a href="index.php?query1">Q1. Display content of "book" table.</a></p>
            <p><a href="index.php?query2">Q2. Display content of "genres" table.</a></p>
            <p><a href="index.php?query3">Q3. Display content of "publishers" table.</a></p>
            <p><a href="index.php?query4">Q4. Display content of "authors" table.</a></p>
            <p><a href="index.php?query5">Q5. Display content of "book_authors" intermediary table.</a></p>
        </div>
        <div>
            <p><?php echo $content ?></p>
        </div>
    </body>
</html>
