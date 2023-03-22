#!/bin/env bash
if [ ! -f pve_creds.env ]; then
	echo "Credentials file doesn't already exist, loading from Bitwarden."
	echo "Logging into bitwarden"
	bw login
	echo "Getting the terraform creds"
	bw get notes pve_terraform_cred > pve_creds.env
fi