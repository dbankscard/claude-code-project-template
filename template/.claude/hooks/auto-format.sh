#!/bin/bash
# Auto-format hook - runs after file edits

# Get the file that was edited
FILE_PATH="$1"

# Skip if no file path provided
if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Get file extension
EXT="${FILE_PATH##*.}"

# Format based on file type
case "$EXT" in
    py)
        # Python files - run black and isort if available
        if command -v black &> /dev/null; then
            black "$FILE_PATH" 2>/dev/null
        fi
        if command -v isort &> /dev/null; then
            isort "$FILE_PATH" 2>/dev/null
        fi
        ;;
    js|jsx|ts|tsx)
        # JavaScript/TypeScript files - run prettier if available
        if command -v prettier &> /dev/null; then
            prettier --write "$FILE_PATH" 2>/dev/null
        fi
        ;;
    json)
        # JSON files - run jq if available
        if command -v jq &> /dev/null; then
            jq . "$FILE_PATH" > "$FILE_PATH.tmp" 2>/dev/null && mv "$FILE_PATH.tmp" "$FILE_PATH"
        fi
        ;;
    md)
        # Markdown files - run prettier if available
        if command -v prettier &> /dev/null; then
            prettier --write "$FILE_PATH" 2>/dev/null
        fi
        ;;
esac

exit 0