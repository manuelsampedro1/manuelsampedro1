.PHONY: test lint build verify

test: verify

lint: verify

build: verify

verify:
	bash scripts/verify_profile.sh
