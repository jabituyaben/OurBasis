<?php
//api/v1/file_upload
$uploaddir = 'uploads/';
file_put_contents( "pulsedata.dat", file_get_contents("php://input"));

echo '{"upload":{"id": "User1234567890"}}';

?>
