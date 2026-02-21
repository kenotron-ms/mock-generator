#!/bin/bash
# Capture a screenshot using macOS screencapture with Chrome
# iPhone 14 viewport: 390x844

osascript <<EOF
tell application "Google Chrome"
    activate
    
    -- Open dev tools and set to mobile view
    set theURL to "http://localhost:5173"
    
    -- Check if window with URL exists
    set windowFound to false
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t contains "localhost:5173" then
                set windowFound to true
                set active tab index of w to index of t
                set index of w to 1
            end if
        end repeat
    end repeat
    
    -- If not found, open new window
    if not windowFound then
        make new window
        set URL of active tab of front window to theURL
    end if
    
    delay 2
end tell

-- Take screenshot of the frontmost window
do shell script "screencapture -l$(osascript -e 'tell app \"Google Chrome\" to id of window 1') /Users/ken/workspace/mock-generator/output/current-app-screenshot.png"
EOF

echo "Screenshot saved to output/current-app-screenshot.png"
