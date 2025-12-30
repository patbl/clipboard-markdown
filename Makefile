all: bin/html-clipboard logos/clipboard-md.icns logos/clipboard-n.icns

apps: all bin/markdownify-clipboard bin/normalize-clipboard
	./build-apps.sh

install: apps
	./install-apps.sh

bin/html-clipboard: src/html-clipboard.swift
	swiftc src/html-clipboard.swift -o bin/html-clipboard

logos/clipboard-md.icns: logos/clipboard-md.png
	mkdir -p logos/clipboard-md.iconset
	@for size in 16 32 128 256 512; do \
		sips -z $$size $$size logos/clipboard-md.png --out logos/clipboard-md.iconset/icon_$${size}x$${size}.png; \
		double=$$((size * 2)); \
		sips -z $$double $$double logos/clipboard-md.png --out logos/clipboard-md.iconset/icon_$${size}x$${size}@2x.png; \
	done
	iconutil -c icns logos/clipboard-md.iconset -o logos/clipboard-md.icns

logos/clipboard-n.icns: logos/clipboard-n.png
	mkdir -p logos/clipboard-n.iconset
	@for size in 16 32 128 256 512; do \
		sips -z $$size $$size logos/clipboard-n.png --out logos/clipboard-n.iconset/icon_$${size}x$${size}.png; \
		double=$$((size * 2)); \
		sips -z $$double $$double logos/clipboard-n.png --out logos/clipboard-n.iconset/icon_$${size}x$${size}@2x.png; \
	done
	iconutil -c icns logos/clipboard-n.iconset -o logos/clipboard-n.icns

clean:
	rm -f bin/html-clipboard
	rm -f logos/*.icns
	rm -rf logos/*.iconset
	rm -rf "Markdownify Clipboard.app"
	rm -rf "Normalize Clipboard.app"

.PHONY: all apps install clean
