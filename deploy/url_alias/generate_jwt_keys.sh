#!/bin/bash
mkdir -p jwt_keys

openssl genrsa -out jwt_keys/jwt_private.pem 2048

openssl rsa -in jwt_keys/jwt_private.pem -pubout -out jwt_keys/jwt_public.pem

chmod 600 jwt_keys/jwt_private.pem
chmod 644 jwt_keys/jwt_public.pem

echo "JWT keys generated in keys directory:"
echo "- jwt_keys/jwt_private.pem - Private key for signing tokens"
echo "- jwt_keys/jwt_public.pem - Public key for verifying tokens"
