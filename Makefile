.DEFAULT_GOAL := help
PORT ?= 1313

.PHONY: help serve new build clean lint fix spell links check update

help: ## Show this help
	@grep -hE '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'

serve: ## Live server w/ draft & opens a browser (override: make serve PORT=8080)
	hugo server --buildDrafts --openBrowser --navigateToChanged --port $(PORT)

build: ## Production build into ./public
	hugo --gc --minify

clean: ## Delete build output and caches
	rm -rf public resources .hugo_build.lock

# === Checks ===
lint: ## Lint Markdown (config @ .markdownlint-cli2.yaml)
	markdownlint-cli2

fix: ## Apply the Markdown fixes markdownlint can make safely
	markdownlint-cli2 --fix

spell: ## Spell-check content and config
	typos

# BTW, this runs after a build so it sees rendered HTML (yay)
links: build ## Check outbound links in the built site
	lychee --no-progress --root-dir "$(CURDIR)/public" \
	  --exclude '^https://kasader\.github\.io' public

check: lint spell build ## Gate before pushing: lint, spell-check, then build

# === Theme ===
update: ## Update the Zen theme module to its latest release
	hugo mod get -u
	hugo mod tidy
