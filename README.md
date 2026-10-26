```
{
  "description": "inference-hook-dlp hooks",
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python \"${CLAUDE_PLUGIN_ROOT}/client/hook.py\" SessionStart",
            "timeout": 20,
            "statusMessage": "Loading usage restrictions"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python \"${CLAUDE_PLUGIN_ROOT}/client/hook.py\" UserPromptSubmit",
            "timeout": 20,
            "statusMessage": "Checking prompt against usage restrictions"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Read|Edit|Write|MultiEdit|NotebookEdit|Bash|Grep|Glob|WebFetch|WebSearch|mcp__.*",
        "hooks": [
          {
            "type": "command",
            "command": "python \"${CLAUDE_PLUGIN_ROOT}/client/hook.py\" PreToolUse",
            "timeout": 30,
            "statusMessage": "Checking tool input against usage restrictions"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Read|Bash|Grep|WebFetch|mcp__.*",
        "hooks": [
          {
            "type": "command",
            "command": "python \"${CLAUDE_PLUGIN_ROOT}/client/hook.py\" PostToolUse",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
``
