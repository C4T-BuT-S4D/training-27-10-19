#!/bin/bash

cd /app

echo "[*] Cleaning deploy"
rm -rf /deploy/*

echo "[*] Building project..."
dotnet publish -c Release -o /deploy/src

echo "[*] Cleaning pdb..."
rm -rf /deploy/src/*.pdb

echo "[*] Copying configuration..."
cp /app/docker_config/* /deploy/

echo "[+] Done!"