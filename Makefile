PYTHON := .venv/bin/python
PYTEST := .venv/bin/pytest
VERSION := $(shell jq -r .version .claude-plugin/plugin.json)

.PHONY: help sync-cases sync-slides gen-case-catalog test test-routing test-anti-patterns test-quality lint typecheck package publish clean

help:
	@echo "Available commands:"
	@echo "  make sync-cases       - Pull 63 cases from airoasting.github.io/5color"
	@echo "  make sync-slides      - Pull 35 templates from airoasting.github.io/slide_library"
	@echo "  make test             - Run all tests"
	@echo "  make test-routing     - Routing accuracy tests (189)"
	@echo "  make test-anti-patterns - Anti-pattern unit tests (50)"
	@echo "  make test-quality     - Quality integration tests (15)"
	@echo "  make lint             - ruff check"
	@echo "  make typecheck        - mypy check"
	@echo "  make package          - Build distributable .zip"
	@echo "  make publish          - Create GitHub release"
	@echo "  make clean            - Remove caches and dist/"

gen-case-catalog:
	$(PYTHON) -m scripts.gen_case_catalog \
		--cases skills/roasting/references/cases/ \
		--out docs/ko/case-catalog.md

sync-cases:
	$(PYTHON) -m scripts.sync_cases \
		--source https://airoasting.github.io/5color/ \
		--out skills/roasting/references/cases/

sync-slides:
	$(PYTHON) -m scripts.sync_slides \
		--source https://airoasting.github.io/slide_library/ \
		--out skills/roasting/references/slide-templates/index.json

test: test-routing test-anti-patterns test-quality

test-routing:
	$(PYTEST) tests/routing/ -v

test-anti-patterns:
	$(PYTEST) tests/anti_patterns/ -v

test-quality:
	$(PYTEST) tests/quality/ -v --slow

lint:
	.venv/bin/ruff check .

typecheck:
	.venv/bin/mypy scripts/

package:
	mkdir -p dist/
	zip -r dist/roasting-$(VERSION).zip \
		.claude-plugin/ skills/ scripts/ README.md README.ko.md LICENSE CHANGELOG.md

publish:
	gh release create v$(VERSION) \
		dist/roasting-$(VERSION).zip \
		--title "v$(VERSION)" \
		--notes-file CHANGELOG.md

clean:
	rm -rf dist/ .pytest_cache/ .mypy_cache/ .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
