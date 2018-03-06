#!/bin/bash

# this script expects 1 parameter: The keyspace's name
usage="$(basename "$0") [-k keyspace]\n
\n
where:\n
    \t-k  company/keyspace to create\n"

keyspace=""
while getopts ':h:k:' option; do
  case "$option" in
    # get company name -- to be used as keyspace
    k) keyspace=$OPTARG
       ;;
    :) printf "missing argument for -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
  esac
done

if [ -z "$keyspace" ]; then
   echo -e $usage
   exit 1
fi


# default path to the table script
path="."

# susbtitute the string $KEYSPACE to the company's name
str_ready=`sed -e "s|\\\$KEYSPACE|$keyspace|g" create_tables_hive.hql`

# execute queries
echo -e "$str_ready\n" | hive -e

# success message
echo "Cassandra was successfully configurated"

