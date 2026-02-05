.PHONY: help build build-simple test clean install

help:
	@echo "onion.press Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  make build        - Build DMG with custom window (requires UI)"
	@echo "  make build-simple - Build DMG without customization (faster)"
	@echo "  make test         - Test the app bundle locally"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make install      - Install app to /Applications (for testing)"
	@echo ""

build:
	@echo "Building DMG with customization..."
	./build/build-dmg.sh

build-simple:
	@echo "Building simple DMG..."
	./build/build-dmg-simple.sh

test:
	@echo "Testing app bundle..."
	@echo "Checking structure..."
	@test -d Onion.Press.app/Contents/MacOS || (echo "ERROR: MacOS directory missing" && exit 1)
	@test -f Onion.Press.app/Contents/MacOS/launcher || (echo "ERROR: launcher missing" && exit 1)
	@test -f Onion.Press.app/Contents/MacOS/onion.press || (echo "ERROR: onion.press script missing" && exit 1)
	@test -f Onion.Press.app/Contents/Info.plist || (echo "ERROR: Info.plist missing" && exit 1)
	@test -f Onion.Press.app/Contents/Resources/docker/docker-compose.yml || (echo "ERROR: docker-compose.yml missing" && exit 1)
	@test -f Onion.Press.app/Contents/Resources/scripts/menubar.py || (echo "ERROR: menubar.py missing" && exit 1)
	@test -f Onion.Press.app/Contents/Resources/scripts/key_manager.py || (echo "ERROR: key_manager.py missing" && exit 1)
	@test -f Onion.Press.app/Contents/Resources/scripts/bip39_words.py || (echo "ERROR: bip39_words.py missing" && exit 1)
	@echo "All required source files present"
	@echo ""
	@echo "Checking MenubarApp bundle..."
	@if [ -d Onion.Press.app/Contents/Resources/MenubarApp ]; then \
		test -f Onion.Press.app/Contents/Resources/MenubarApp/Contents/MacOS/menubar || \
			(echo "ERROR: MenubarApp executable missing" && exit 1); \
		echo "MenubarApp bundle present"; \
	else \
		echo "NOTE: MenubarApp not yet built (run make build-simple)"; \
	fi
	@echo ""
	@echo "Checking permissions..."
	@test -x Onion.Press.app/Contents/MacOS/launcher || (echo "ERROR: launcher not executable" && exit 1)
	@test -x Onion.Press.app/Contents/MacOS/onion.press || (echo "ERROR: onion.press not executable" && exit 1)
	@echo "Permissions correct"
	@echo ""
	@echo "App bundle structure is valid!"
	@echo "To run locally: open Onion.Press.app"

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/*.dmg
	rm -rf build/temp.dmg
	rm -rf Onion.Press.app/Contents/Resources/MenubarApp
	@echo "Build artifacts cleaned"

install:
	@echo "Installing to /Applications..."
	@if [ -d "/Applications/Onion.Press.app" ]; then \
		echo "Removing existing installation..."; \
		rm -rf "/Applications/Onion.Press.app"; \
	fi
	cp -R Onion.Press.app /Applications/
	@echo "Installed to /Applications/Onion.Press.app"
	@echo "You can now launch it from Applications or Spotlight"
