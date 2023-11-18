test:
	pytest tests

test_coverage:
	COVERAGE_FILE=/tmp/.coverage pytest -vv --cov=merkle_zeppelin

install_pre_commit_hooks:
	pre-commit install -c .github/pre-commit-config.yaml

update_pre_commit_hooks:
	pre-commit install -c .github/pre-commit-config.yaml
