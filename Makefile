.PHONY: install-git-syntax install

# Installing lib for checking syntax of commits
install-git-syntax:
	cp -R ./Infra/GitSyntax/* ./.git/hooks

# Installind all dependances
install: install-git-syntax
