# S16-Leads Makefile
# ==================

.PHONY: install test test-limiter test-fast run-security-check clean setup-dirs help sync-env check-env

# Default target
help:
	@echo "Available targets:"
	@echo "  sync-env        - Sync .env from env.sample (add missing keys)"
	@echo "  check-env       - Check what's missing in .env"
	@echo "  install         - Install dependencies"
	@echo "  setup-dirs      - Create required directories"
	@echo "  test            - Run all tests"
	@echo "  test-limiter    - Run only anti-spam limiter tests"
	@echo "  test-fast       - Run tests without slow integration tests"
	@echo "  run-security    - Run security check script"
	@echo "  clean           - Clean up temporary files"

# Sync .env from env.sample - добавляет недостающие ключи
sync-env:
	@echo "🔧 Syncing .env from .env.sample..."
	@if [ ! -f .env ]; then \
		echo "📁 Creating .env from .env.sample"; \
		cp .env.sample .env; \
		echo "✅ .env created with all default values"; \
	else \
		echo "📝 Checking for missing keys in .env..."; \
		python3 scripts/sync_env.py; \
	fi

# Check what's missing in .env without modifying
check-env:
	@echo "🔍 Checking .env completeness..."
	@if [ ! -f .env ]; then \
		echo "❌ .env file does not exist"; \
		echo "💡 Run 'make sync-env' to create it"; \
	else \
		python3 scripts/check_env.py; \
	fi

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

# Set up required directories
setup-dirs:
	@echo "📁 Creating directories..."
	mkdir -p data/sessions data/export data/anti_spam data/logs
	chmod 700 data/sessions
	@echo "✅ Directories created"

# Run all tests
test: install
	@echo "🧪 Running all tests..."
	python -m pytest tests/ -v

# Run only anti-spam limiter tests
test-limiter: install
	@echo "🧪 Running anti-spam limiter tests..."
	python -m pytest tests/test_limiter.py -v

# Run fast tests (skip slow integration tests)
test-fast: install
	@echo "🧪 Running fast tests..."
	python -m pytest tests/ -v -m "not slow"

# Run security check
run-security:
	@echo "🔒 Running security check..."
	python scripts/security_check.py

# Clean temporary files
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -f test_export.json
	@echo "✅ Cleanup complete"

# Development setup
dev-setup: sync-env setup-dirs install
	@echo "🚀 Development environment ready!"
	@echo "💡 Next steps:"
	@echo "  1. Edit .env with your API credentials"
	@echo "  2. Run 'make test-limiter' to test anti-spam system"
	@echo "  3. Run 'make check-env' to verify configuration"

# Check anti-spam status
check-anti-spam:
	@echo "🛡️  Checking anti-spam system status..."
	@python -c "from src.infra.limiter import get_rate_limiter; limiter = get_rate_limiter(); print('📊 Stats:', limiter.get_stats())" 2>/dev/null || echo "❌ Anti-spam system not initialized"

# Show current .env status
env-status: check-env check-anti-spam

# CLI shortcuts (require GROUP_ID variable)
info:
	@if [ -z "$(GROUP_ID)" ]; then echo "❌ Usage: make info GROUP_ID=-1001234567890"; exit 1; fi
	PYTHONPATH=. python src/cli.py info $(GROUP_ID)

participants:
	@if [ -z "$(GROUP_ID)" ]; then echo "❌ Usage: make participants GROUP_ID=-1001234567890 LIMIT=100"; exit 1; fi
	PYTHONPATH=. python src/cli.py participants $(GROUP_ID) --limit $(or $(LIMIT),100)

export:
	@if [ -z "$(GROUP_ID)" ]; then echo "❌ Usage: make export GROUP_ID=-1001234567890 OUTPUT=data/export/members.json"; exit 1; fi
	PYTHONPATH=. python src/cli.py export $(GROUP_ID) --output $(or $(OUTPUT),data/export/members.json) --format $(or $(FORMAT),json)
