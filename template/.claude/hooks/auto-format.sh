#!/bin/bash
# Auto-format hook - Automatically formats code on save/commit

set -e

echo "🎨 Running auto-formatter..."

# Detect changed files
if [ -n "$1" ]; then
    # Specific files provided
    FILES="$@"
else
    # Get staged files from git
    FILES=$(git diff --cached --name-only --diff-filter=ACM)
fi

# Python formatting with Black
format_python() {
    local file="$1"
    echo "  Formatting Python: $file"
    
    # Check if black is installed
    if command -v black &> /dev/null; then
        black "$file" --quiet
    else
        echo "  ⚠️  Black not installed, skipping Python formatting"
        return 0
    fi
    
    # Sort imports with isort
    if command -v isort &> /dev/null; then
        isort "$file" --quiet
    fi
}

# JavaScript/TypeScript formatting with Prettier
format_javascript() {
    local file="$1"
    echo "  Formatting JS/TS: $file"
    
    # Check if prettier is installed
    if command -v prettier &> /dev/null; then
        prettier --write "$file" --log-level=error
    elif [ -f "node_modules/.bin/prettier" ]; then
        ./node_modules/.bin/prettier --write "$file" --log-level=error
    else
        echo "  ⚠️  Prettier not installed, skipping JS/TS formatting"
        return 0
    fi
}

# Go formatting
format_go() {
    local file="$1"
    echo "  Formatting Go: $file"
    
    if command -v gofmt &> /dev/null; then
        gofmt -w "$file"
    else
        echo "  ⚠️  gofmt not installed, skipping Go formatting"
        return 0
    fi
}

# Rust formatting
format_rust() {
    local file="$1"
    echo "  Formatting Rust: $file"
    
    if command -v rustfmt &> /dev/null; then
        rustfmt "$file" --quiet
    else
        echo "  ⚠️  rustfmt not installed, skipping Rust formatting"
        return 0
    fi
}

# YAML formatting
format_yaml() {
    local file="$1"
    echo "  Formatting YAML: $file"
    
    # Use prettier if available
    if command -v prettier &> /dev/null; then
        prettier --write "$file" --log-level=error
    elif command -v yamlfmt &> /dev/null; then
        yamlfmt "$file"
    fi
}

# JSON formatting
format_json() {
    local file="$1"
    echo "  Formatting JSON: $file"
    
    # Use jq for formatting
    if command -v jq &> /dev/null; then
        jq . "$file" > "$file.tmp" && mv "$file.tmp" "$file"
    elif command -v prettier &> /dev/null; then
        prettier --write "$file" --log-level=error
    fi
}

# Markdown formatting
format_markdown() {
    local file="$1"
    echo "  Formatting Markdown: $file"
    
    if command -v prettier &> /dev/null; then
        prettier --write "$file" --log-level=error
    elif command -v markdownlint &> /dev/null; then
        markdownlint --fix "$file"
    fi
}

# CSS/SCSS formatting
format_css() {
    local file="$1"
    echo "  Formatting CSS/SCSS: $file"
    
    if command -v prettier &> /dev/null; then
        prettier --write "$file" --log-level=error
    elif command -v stylelint &> /dev/null; then
        stylelint --fix "$file"
    fi
}

# Process each file
formatted_count=0
for file in $FILES; do
    # Skip if file doesn't exist (deleted)
    [ -f "$file" ] || continue
    
    # Get file extension
    extension="${file##*.}"
    filename="${file##*/}"
    
    # Apply appropriate formatter
    case "$extension" in
        py)
            format_python "$file"
            ((formatted_count++))
            ;;
        js|jsx|ts|tsx)
            format_javascript "$file"
            ((formatted_count++))
            ;;
        go)
            format_go "$file"
            ((formatted_count++))
            ;;
        rs)
            format_rust "$file"
            ((formatted_count++))
            ;;
        yml|yaml)
            format_yaml "$file"
            ((formatted_count++))
            ;;
        json)
            # Skip package-lock.json and similar
            if [[ "$filename" != *"-lock.json" ]]; then
                format_json "$file"
                ((formatted_count++))
            fi
            ;;
        md)
            format_markdown "$file"
            ((formatted_count++))
            ;;
        css|scss|sass)
            format_css "$file"
            ((formatted_count++))
            ;;
    esac
done

# Re-stage formatted files if running as pre-commit hook
if [ -n "$GIT_EXEC_PATH" ]; then
    for file in $FILES; do
        [ -f "$file" ] && git add "$file"
    done
fi

if [ $formatted_count -gt 0 ]; then
    echo "✅ Formatted $formatted_count files"
else
    echo "✅ No files needed formatting"
fi

# Check for formatting tools and suggest installation
check_tools() {
    local missing_tools=()
    
    # Check Python tools
    if [ -n "$(find . -name "*.py" -type f 2>/dev/null | head -1)" ]; then
        command -v black &> /dev/null || missing_tools+=("black")
        command -v isort &> /dev/null || missing_tools+=("isort")
    fi
    
    # Check JS/TS tools
    if [ -n "$(find . -name "*.js" -o -name "*.ts" -type f 2>/dev/null | head -1)" ]; then
        command -v prettier &> /dev/null || [ -f "node_modules/.bin/prettier" ] || missing_tools+=("prettier")
    fi
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        echo ""
        echo "💡 Tip: Install these formatters for better code formatting:"
        for tool in "${missing_tools[@]}"; do
            case "$tool" in
                black|isort)
                    echo "  pip install $tool"
                    ;;
                prettier)
                    echo "  npm install --save-dev prettier"
                    ;;
            esac
        done
    fi
}

# Only check tools occasionally to avoid spam
if [ "$((RANDOM % 10))" -eq 0 ]; then
    check_tools
fi

exit 0