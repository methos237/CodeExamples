<?php
/**
 * CSC 471 HW 3 / Dr. Fred Sadri / UNCG
 * @author James Knox Polk <jkpolk@uncg.edu>
 * Date: 2/21/2019
 */

$content = "Please click on a query to run";

$args = explode('=', rtrim($_SERVER['QUERY_STRING'], '/'));
$method = array_shift($args);


if (isset($_GET["submit"])){
    print ($_GET["course"]);
}

switch($method) {
    case 'query1':
        $content = "<table class='w3-table-all'>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                        </tr>";
        foreach (query1 () as $data){
            $content .= "<tr><td>".$data['id']."</td><td>".$data['name']."</td></tr>";
        }
        $content.="</table>";
        break;
    case 'query2':
        $content = "<table class='w3-table-all'>
                        <tr>
                            <th>Course Number</th>
                            <th>Title</th>
                        </tr>";
        foreach (query2 () as $data){
            $content .= "<tr><td>".$data['cNo']."</td><td>".$data['title']."</td></tr>";
        }
        $content.="</table>";
        break;
    case 'query3':
        $content = "<table class='w3-table-all'>
                        <tr>
                            <th>Name</th>
                            <th>Total Credits</th>
                            <th>ID</th>
                            
                        </tr>";
        foreach (query3 () as $data){
            $content .= "<tr><td>".$data['name']."</td><td>".$data['total_credits']."</td><td>".$data['id']."</td></tr>";
        }
        $content.="</table>";;
        break;
    case 'course':
        $course = $args[0];
        $content = "<table class='w3-table-all'>
                        <tr>
                            <th>Name</th>
                            <th>Grade</th>
                        </tr>";
        foreach (query4 ( $course) as $data){
            $content .= "<tr><td>".$data['name']."</td><td>".$data['grade']."</td></tr>";
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
        <title>CSC 471 HW 3 / Dr. Fred Sadri / UNCG</title>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    </head>
    <body>
    <h1>CSC 471 HW 3 / Dr. Fred Sadri / UNCG</h1>
    <div>
        <p><?php echo $content ?></p>
    </div>
    <div>
        <p><a href="index.php?query1">Q1. List all students (ids and names) in CS department.</a></p>
        <p><a href="index.php?query2">Q2. List all courses (cNos and titles) “Cindy” has taken, and passed with a grade of “A” or “B”.</a></p>
        <p><a href="index.php?query3">Q3. List students in CS department, and for each student list the total credit-hours the student
                has taken (hence, the output table has three columns: id, name, total
                credits).</a></p>
        <div><form name="Q4." method="get" action="<?php echo $_SERVER['PHP_SELF']; ?>">
                <p>Q4. Display all students (names) who have taken the course you enter below, and the
                grade they received in that course.</p>
                <p><label for="course">Course</label><input type="text" name="course"></p>
                <p><input type="submit"></p>
        </form> </div>
    </div>
    </body>
</html>
<?php
function  query1 () {
    $db = DBConnect::instance ();
    $data = $db->getAll ("SELECT id, name FROM students WHERE dept = 'CS'");
    return $data;
}

function query2 () {
    $db = DBConnect::instance ();
    $data = $db->getAll ("SELECT distinct courses.cNo, courses.title
                                FROM
                                  courses
                                  INNER JOIN transcripts ON transcripts.cNo = courses.cNo,
                                  students
                                WHERE
                                  (students.name = 'Cindy' AND
                                  transcripts.grade = 'A') OR
                                  (transcripts.grade = 'B')");
    return $data;
}

function query3 () {
    $db = DBConnect::instance ();
    $data = $db->getAll ("SELECT students.name, Sum(DISTINCT courses.credits) AS total_credits, transcripts.id
                                FROM
                                  courses
                                  INNER JOIN transcripts ON transcripts.cNo = courses.cNo
                                  INNER JOIN students ON transcripts.id = students.id
                                WHERE
                                  students.dept = 'CS'
                                GROUP BY
                                  students.name,
                                  transcripts.id");
    return $data;
}

function query4 ($_cTitle) {
    $db = DBConnect::instance ();
    $data = $db->getAll ("SELECT DISTINCT students.name, transcripts.grade
                                FROM
                                  students
                                  INNER JOIN transcripts ON transcripts.id = students.id
                                  INNER JOIN courses ON transcripts.cNo = courses.cNo
                                WHERE
                                  courses.title = '$_cTitle'");
    return $data;
}


function print_r2 ( $_val ) {
    echo '<pre>';
    print_r ($_val);
    echo '</pre>';
}


/**
 * DBConnect Class
 *
 * Last Updated: 9/25/2018
 *
 * Description: Wrapper class for PDO database operations.
 *
 * @author James Knox Polk <jkpolk@uncg.edu>
 *
 */


class DBConnect {
    private $debug;
    private $killOnError;
    private $options;
    protected static $instance;
    protected $pdo;
    protected $host = 'localhost';
    protected $dbName = 'test';
    protected $charSet = 'utf8mb4';
    protected $dbUser = 'root';
    protected $dbPass = '';

    protected function __construct () {
        $host = $this->host;
        $dbName = $this->dbName;
        $charSet = $this->charSet;
        $dbUser = $this->dbUser;
        $dbPass = $this->dbPass;

        $this -> debug = TRUE;
        $this -> killOnError = FALSE;
        $this -> options = array (
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => FALSE,
        );
        $dsn = "mysql:host=$host;dbname=$dbName;charset=$charSet";
        $this -> pdo = new PDO( $dsn, $dbUser, $dbPass, $this -> options );
    }
    /**
     * Public access to DBConnect class
     *
     * @return DBConnect
     */
    public static function instance () {
        if ( self ::$instance === NULL ) {
            self ::$instance = new self;
        }
        return self ::$instance;
    }
    /**
     * Proxy to native PDO methods
     *
     * @param $_method
     * @param $_args
     *
     * @return mixed
     */
    public function __call ( $_method, $_args ) {
        return call_user_func_array ( array ( $this -> pdo, $_method ), $_args );
    }
    /**
     * Helper function to smoothly run prepared statements
     *
     * @param       $_sql
     * @param array $_args
     *
     * @return bool|\PDOStatement
     */
    public function run ( $_sql, $_args = [] ) {
        try {
            if ( !$_args ) {
                return $this -> pdo->query ( $_sql );
            }
            $stmt = $this -> pdo -> prepare ( $_sql );
            $stmt -> execute ( $_args );
        } catch ( PDOException $e ) {
            $this -> handleError ( $e -> getMessage () );
            throw  $e;
        }
        return $stmt;
    }
    /**
     * Helper function to return one record from a database table
     *
     * @param       $_sql
     * @param array $_args
     *
     * @return mixed
     */
    public function getOne ( $_sql, $_args = [] ) {
        $data = $this -> run ( $_sql, $_args ) -> fetch ();
        return $data;
    }
    /**
     * Helper function to return all records from a database table
     *
     * @param       $_sql
     * @param array $_args
     *
     * @return array
     */
    public function getAll ( $_sql, $_args = [] ) {
        $data = $this -> run ( $_sql, $_args ) -> fetchAll ();
        return $data;
    }
    /**
     * Error handler for all database calls
     *
     * @param string $_error
     */
    private function handleError ( string $_error ): void {
        error_log ( $_error );
        if ( $this -> debug ) {
            echo $_error;
        }
        if ( $this -> killOnError ) {
            die( $_error );
        }
    }
}