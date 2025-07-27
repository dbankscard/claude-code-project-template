---
name: plan
namespace: project
description: Project planning and architecture design
---

# Project Planning Command

Invokes the planning-architect for comprehensive project planning.

## Usage
```
/project:plan <objective> [--scope feature|module|system] [--output markdown|mermaid|both]
```

## Planning Process
1. **Requirements Analysis**: Breaks down objectives
2. **Architecture Design**: Creates system design
3. **Task Breakdown**: Identifies implementation tasks
4. **Risk Assessment**: Evaluates potential challenges
5. **Timeline Estimation**: Provides effort estimates

## Options
- `--scope`: Planning scope (default: feature)
  - `feature`: Single feature planning
  - `module`: Module or service planning
  - `system`: Full system architecture
- `--output`: Output format (default: markdown)

## Example
```
/project:plan "Add real-time notifications" --scope feature --output both
```

## Deliverables
- Architecture diagrams
- Component specifications
- Task breakdown structure
- Risk mitigation strategies
- Implementation roadmap