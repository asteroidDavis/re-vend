#!/bin/bash

#database is the only argument
$database = $1

#syncs the database to the ec2 instance using rsync
rsync -avz --progress --stats /var/lib/msql/$1 ec2-user@ec2-52-1-65-45.compute-1.amazonaws.com:/var/lib/msql/$1


