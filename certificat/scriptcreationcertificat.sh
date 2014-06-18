#!/bin/sh
# Automation create of certificat
# Usage : ./scriptcreationcertificat.sh domain.com

domain = $1

# Creation of private key
# openssl genrsa -out masterca.key 2048
openssl genrsa -des3 -out masterca.key 2048
echo "Master Key generate"

# Creation of csr
openssl req -new -key masterca.key -out $1.csr
echo "Csr create"

# Testing csr
openssl req -noout -text -in $1.csr
echo "CSR OK"

# Self signed the csr to get the certificat
openssl x509 -req -days 365 -in $1.csr -signkey masterca.key -out $1.crt
echo "Certificat self signed"