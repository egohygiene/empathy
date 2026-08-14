<?php

$config = require '/action/lib/.automation/.php-cs-fixer.dist.php';
$config->getFinder()->exclude(['.cache', '.git', '.reports', '.reports/megalinter']);
return $config;
