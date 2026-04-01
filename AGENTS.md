# AGENTS.md - Root Repository Guide

This document is the **MASTER GUIDE** for AI agents operating in this monorepo. It provides an overview of all applications, initialization instructions, and rules that apply to ALL apps in this repository.

---

## 🏠 Repository Overview

**Repository Type**: Multi-App Monorepo (React SPA Projects)
**Location**: `C:\Users\Tan\OneDrive - Hanoi University of Science and Technology\Documents\WebAgent\my-app`
**Structure**: Each app is a standalone React project with its own `package.json`, `node_modules`, and dependencies.

---

## 📱 Available Applications

This repository contains the following applications:

### 1. Sidebar App
| Property | Value |
|----------|-------|
| **Folder** | `Sidebar app/` |
| **Purpose** | Demonstrates a vertical sidebar navigation component |
| **Stack** | React 19, Express 5, react-router-dom 7 |
| **React Port** | 3000 |
| **Backend Port** | 5000 |
| **Main Components** | Sidebar, Home |
| **Color Theme** | Dark sidebar with #2c3e50 background |
| **AGENTS.md** | `Sidebar app/AGENTS.md` |

**Components**:
- `Sidebar.js` / `Sidebar.css` - Vertical navigation sidebar
- `Home.js` - Home page content
- `App.js` - Main app wrapper

---

### 2. Horizontal Navigation Bar App
| Property | Value |
|----------|-------|
| **Folder** | `Horizontal Navigation Bar app/` |
| **Purpose** | Demonstrates a horizontal navigation bar with interactive components |
| **Stack** | React 19, Express 5, react-router-dom 7 |
| **React Port** | 3000 |
| **Backend Port** | 5001 |
| **Main Components** | NavBar, Home, Button, Dropdown |
| **Color Theme** | Blue navigation (#3498db) with gradient header |
| **AGENTS.md** | `Horizontal Navigation Bar app/AGENTS.md` |

**Components**:
- `NavBar.js` / `NavBar.css` - Horizontal navigation bar
- `Home.js` / `Home.css` - Landing page with demos
- `Button.js` / `Button.css` - Multi-variant buttons (primary, secondary, success, danger)
- `Dropdown.js` / `Dropdown.css` - Interactive dropdown menu

**Color Palette**:
| Element | Hex Code |
|---------|----------|
| Primary Blue | #3498db |
| Dark Blue | #2c3e50 |
| Success Green | #27ae60 |
| Danger Red | #e74c3c |
| Light Gray | #ecf0f1 |

---

## 🚀 Initialization Instructions (FOR AGENTS)

### How to Initialize Individual Apps

Each app requires initialization before use. Follow these steps carefully:

#### Step 1: Navigate to App Directory
```bash
# For Sidebar App
cd "Sidebar app"

# For Horizontal Navigation Bar App
cd "Horizontal Navigation Bar app"
```

#### Step 2: Install Dependencies
```bash
npm install
```

#### Step 3: Start Development Servers

**For Sidebar App:**
```bash
# Terminal 1: React frontend
npm start

# Terminal 2: Express backend
node server.js
```
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

**For Horizontal Navigation Bar App:**
```bash
# Terminal 1: React frontend
npm start

# Terminal 2: Express backend
node server.js
```
- Frontend: http://localhost:3000
- Backend: http://localhost:5001

#### Step 4: Build for Production
```bash
npm run build
```
- Output: `/build` folder
- Ready to deploy

---

### Quick Start Commands Reference

| App | Install | Frontend | Backend | Build |
|-----|---------|----------|---------|-------|
| Sidebar app | `cd "Sidebar app" && npm install` | `npm start` (port 3000) | `node server.js` (port 5000) | `npm run build` |
| Horizontal Navigation Bar app | `cd "Horizontal Navigation Bar app" && npm install` | `npm start` (port 3000) | `node server.js` (port 5001) | `npm run build` |

---

## 📋 Detailed App-Specific Rules

### For Sidebar App

```
1. ALWAYS read "Sidebar app/AGENTS.md" before working on this app
2. Backend runs on port 5000 - DO NOT use port 5000 for other purposes
3. Component files are in: "Sidebar app/src/components/"
4. CSS files are co-located with components (Sidebar.css with Sidebar.js)
5. Default route: "/" shows Home page
6. No test files exist - add *.test.js alongside components if needed
```

### For Horizontal Navigation Bar App

```
1. ALWAYS read "Horizontal Navigation Bar app/AGENTS.md" before working on this app
2. Backend runs on port 5001 - DO NOT use port 5001 for other purposes
3. Component files are in: "Horizontal Navigation Bar app/src/components/"
4. Available components: NavBar, Home, Button, Dropdown
5. Button variants: primary (blue), secondary (gray), success (green), danger (red)
6. Dropdown supports click-outside-to-close behavior
7. No test files exist - add *.test.js alongside components if needed
```

---

## 🎯 Task Routing Rules

When given a task, route it to the correct app:

| Task Type | Route To |
|-----------|----------|
| "Sidebar navigation", "vertical menu", "side bar" | Sidebar app |
| "Horizontal nav", "top bar", "navbar", "navigation bar" | Horizontal Navigation Bar app |
| "Buttons", "dropdown", "horizontal components" | Horizontal Navigation Bar app |
| "Multiple apps", "add new app", "monorepo" | Root level |
| "Global changes", "affects all apps" | Read ALL AGENTS.md files first |

---

## ⚙️ Global Automation Rules (APPLY TO ALL AGENTS)

### Critical Autonomy Rules
```
1. AUTHORITY: You have FULL PERMISSION to edit any files and run any terminal commands
2. NON-INTERACTIVE: Do NOT ask for confirmation. Do NOT wait for user input
3. AUTOMATIC GIT WORKFLOW: After fixing/implementing:
   - git add .
   - git commit -m "fix: [description]" OR "feat: [description]"
   - git push origin HEAD
4. WINDOWS ENVIRONMENT: Use Windows PowerShell compatible commands
5. NO CONFIRMATION: Just DO IT
```

### Workflow Guidelines
```
1. BEFORE WORKING: Always check which app the task belongs to
2. READ DOCS: Read the app-specific AGENTS.md before making changes
3. IDENTIFY APP: Determine correct app folder from task description
4. MAKE CHANGES: Edit files within the correct app directory
5. VERIFY: Run linter/diagnostics to check for errors
6. TEST: If applicable, run npm test in the app directory
7. REPORT: Create a report about what just did 
8. COMMIT: Use git commands in the app directory
9. PUSH: Push changes to remote repository
```

---

## 🔧 Common Operations

### Adding a New Component to an App

1. Navigate to app directory
2. Read app's AGENTS.md
3. Create component file (e.g., `MyComponent.js`)
4. Create co-located CSS (e.g., `MyComponent.css`)
5. Import and use in parent component
6. Run diagnostics to check for errors

### Switching Between Apps

When working on a different app:
```
1. cd to the new app directory
2. Read that app's AGENTS.md
3. Make your changes
4. Commit from that directory
```

### Port Conflicts

If you encounter port conflicts:
- Sidebar app backend: port 5000
- Horizontal Navigation Bar app backend: port 5001
- React dev servers can both use port 3000 (run separately)

---

## 📁 Directory Structure

```
my-app/
├── .github/                      # GitHub workflows
├── .openclaw/                    # Agent tools configuration
│   └── tools/
│       └── devops.yaml
├── Sidebar app/                  # App 1: Vertical sidebar navigation
│   ├── public/
│   ├── src/
│   │   └── components/
│   │       ├── Home.js
│   │       ├── Sidebar.js
│   │       └── Sidebar.css
│   ├── server.js                 # Backend on port 5000
│   ├── package.json
│   └── AGENTS.md                 # App-specific rules
├── Horizontal Navigation Bar app/ # App 2: Horizontal navigation bar
│   ├── public/
│   ├── src/
│   │   └── components/
│   │       ├── NavBar.js
│   │       ├── NavBar.css
│   │       ├── Home.js
│   │       ├── Home.css
│   │       ├── Button.js
│   │       ├── Button.css
│   │       ├── Dropdown.js
│   │       └── Dropdown.css
│   ├── server.js                 # Backend on port 5001
│   ├── package.json
│   └── AGENTS.md                 # App-specific rules
└── AGENTS.md                     # THIS FILE - Root master guide
```

---

## ❓ Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Kill the process using that port, or use the other app's port |
| Module not found | Run `npm install` in the app directory |
| Changes not showing | Restart the React dev server (`npm start`) |
| Backend not responding | Check if `node server.js` is running in correct directory |
| Wrong app modified | Check `git status` and `git diff` to verify changes |

---

## 📞 Important Reminders

1. **ONE APP AT A TIME**: Work on one app per session if possible
2. **READ AGENTS.MD**: Each app has its own AGENTS.md - always read it first
3. **PORT AWARENESS**: Different backends use different ports
4. **COMMIT FROM APP DIR**: When committing, ensure you're in the correct app directory
5. **NO EJECTING**: Never run `npm eject` in any app

---

## 🔒 Security & Best Practices

```
1. NEVER commit node_modules/ to git (already in .gitignore)
2. NEVER expose API keys or secrets in code
3. Use environment variables (.env files) for sensitive data
4. CRA requires REACT_APP_ prefix for client-side env vars
5. Backend ports should remain internal (not exposed in production)
```

---

**Last Updated**: 2026-04-01
**Total Apps**: 2
**Next Task**: Initialize both apps with `npm install`
## Permissions 
YOU HAVE ACCESS TO THE TERMINAL. PUSHING THE CODE ON GITHUB IS MANDATORY TO COMPLETE THE TASK. DON'T ASK, JUST DO IT.