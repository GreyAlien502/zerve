#!/bin/bash
`dirname $BASH_SOURCE`/zerve &
while :;do
	lt -p8080 --subdomain welcometomyigloo
done
