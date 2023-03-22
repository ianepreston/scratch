#!/bin/env bash
if [ ! -f vault_password ]; then
	echo "Credentials file doesn't already exist, loading from Bitwarden."
	echo "Logging into bitwarden"
	bw login
	bw sync
	echo "Getting the ansible creds"
	bw get notes ansible_vault_password > vault_password
fi