.PHONY: dev start services dev-all ml speech gateway frontend

# Default command: starts speech-service and ml-service
dev:
	node scripts/dev-services.js

start: dev

services: dev

dev-all:
	node scripts/dev-services.js --all

ml:
	node scripts/dev-services.js --ml

speech:
	node scripts/dev-services.js --speech

gateway:
	npm --prefix backend run dev

frontend:
	npm --prefix frontend run dev
