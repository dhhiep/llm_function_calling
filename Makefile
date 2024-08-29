.DEFAULT_GOAL := help

# References:
# - Makefile self documenting
#   https://gist.github.com/prwhite/8168133
.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "; printf "\nUsage: \033[36m\033[0m\n"}; {printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Usage:
# make start_server
start_server: ## Start the server (Ex: make start_server)
	python -m llama_cpp.server --model model/functionary-7b-v2.q4_0.gguf --chat_format functionary-v2 --hf_pretrained_model_name_or_path ./model
