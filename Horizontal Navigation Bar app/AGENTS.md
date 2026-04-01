# AGENTS.md - Codebase Guide

This document provides guidance for AI agents operating in this repository.

## Project Overview

- **App Name**: Horizontal Navigation Bar
- **Purpose**: Demonstrates a modern horizontal navigation bar with interactive components
- **Type**: React SPA with Express backend
- **Stack**: React 19, Express 5, react-router-dom 7
- **Structure**: CRA (Create React App) - ejected configuration NOT used
- **Language**: JavaScript (no TypeScript)

## Project Structure

```
## Project Structure
├── public/           # Static assets (HTML, icons, manifest)
│   └── index.html    # Main HTML template
├── src/
│   ├── components/   # React components
│   │   ├── NavBar.js     # Horizontal navigation bar component
│   │   ├── NavBar.css    # Navigation bar styles
│   │   ├── Home.js       # Home page with component demos
│   │   ├── Home.css      # Home page styles
│   │   ├── Button.js     # Reusable button component
│   │   ├── Button.css    # Button styles (primary, secondary, success, danger)
│   │   └── Dropdown.js   # Interactive dropdown component
│   │   └── Dropdown.css  # Dropdown styles
│   ├── App.js         # Main app component
│   ├── App.css        # App-specific styles
│   ├── index.js       # Entry point
│   └── index.css      # Global styles
├── server.js          # Express backend (port 5001)
└── package.json
```

## App Components

### 1. NavBar Component
- **Purpose**: Horizontal navigation bar at the top of the page
- **Features**:
  - Logo/brand name on the left
  - Navigation menu links (Home, About, Services, Contact)
  - Action buttons (Login, Sign Up)
- **Colors**:
  - Background: #2c3e50 (dark blue-gray)
  - Links: #bdc3c7 (gray), active: #ecf0f1 (white)
  - Primary button: #3498db (blue)
  - Hover states: darker shades

### 2. Home Component
- **Purpose**: Landing page demonstrating all components
- **Features**:
  - Header with gradient background (purple to blue)
  - Section showcasing Button and Dropdown demos
  - Features list with checkmarks
  - Footer with copyright

### 3. Button Component
- **Purpose**: Reusable button with multiple variants
- **Variants**:
  - `primary`: #3498db (blue) - Main actions
  - `secondary`: #95a5a6 (gray) - Secondary actions
  - `success`: #27ae60 (green) - Positive actions
  - `danger`: #e74c3c (red) - Destructive actions
- **Props**: `label` (string), `variant` (string), `onClick` (function)

### 4. Dropdown Component
- **Purpose**: Interactive dropdown menu
- **Features**:
  - Click to toggle open/close
  - Click outside to close
  - Selected item highlighted
  - Customizable options
- **Props**: `options` (array), `placeholder` (string), `onSelect` (function)

## Color Palette

| Element | Color | Hex Code |
|---------|-------|----------|
| Primary Blue | Navigation, Primary Button | #3498db |
| Dark Blue | Navigation Background | #2c3e50 |
| Darker Blue | Primary Hover | #2980b9 |
| Success Green | Success Button | #27ae60 |
| Danger Red | Danger Button | #e74c3c |
| Gray | Secondary Button | #95a5a6 |
| Light Gray | Body Background | #ecf0f1 |
| White | Cards, Content | #ffffff |
| Purple | Header Gradient Start | #8e44ad |

## Build/Lint/Test Commands

```bash
# Development
npm start              # Start React dev server (port 3000)
node server.js        # Start Express backend (port 5001)

# Production
npm run build         # Build optimized bundle to /build

# Testing (Jest + React Testing Library)
npm test              # Run tests in watch mode
npm test -- --watchAll=false           # Run tests once (CI mode)
npm test -- --testPathPattern=Button   # Run single test file matching "Button"
npm test -- --testNamePattern="renders" # Run tests with name containing "renders"
npm test -- --coverage                 # Generate coverage report
```

### Testing Setup

- **Framework**: Jest (via react-scripts)
- **Libraries**: @testing-library/react, @testing-library/user-event, @testing-library/jest-dom
- **Test file pattern**: `*.test.js` or `*.spec.js` (place alongside source files)
- **Example test structure**:
  ```javascript
  import { render, screen } from '@testing-library/react';
  import userEvent from '@testing-library/user-event';
  import Button from './Button';

  test('renders button with label', () => {
    render(<Button label="Click Me" />);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });
  ```

## Code Style Guidelines

### JavaScript Conventions

1. **File naming**: PascalCase for components (`Button.js`), camelCase for utilities
2. **Component naming**: Use PascalCase, match filename
3. **Imports**: Use double quotes for consistency with CRA defaults
4. **Prop destructuring**: Prefer in function parameters
5. **No TypeScript**: Plain JavaScript only

### React Patterns

```javascript
// ✅ Preferred: functional components with arrow functions
const Button = ({ label, variant }) => {
  return <button className={`btn btn--${variant}`}>{label}</button>;
};

// ✅ Preferred: named exports + default export
export const Button = ({ label }) => { ... };
export default Button;

// ✅ Preferred: inline styles use double quotes
<div style={{ display: "flex" }}>

// ❌ Avoid: inline arrow functions in JSX (extract to named functions)
```

### CSS Conventions

1. **BEM-lite**: Use lowercase with hyphens (`.navbar`, `.navbar-item`)
2. **Component CSS**: Co-locate with component (e.g., `Button.css` with `Button.js`)
3. **CSS files**: camelCase naming (`App.css`, `index.css`)
4. **Classes**: BEM-style (`.dropdown__trigger`, `.dropdown__menu`)
5. **Inline styles**: Use double quotes, camelCase properties

### Import Conventions

```javascript
// ✅ React core
import React from "react";

// ✅ Components (relative paths)
import Button from "./components/Button";

// ✅ Icons (named imports from react-icons/fa)
import { FaHome, FaUser } from "react-icons/fa";

// ✅ CSS (co-located or global)
import "./Button.css";
import "./index.css";
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `NavBar`, `Dropdown` |
| Files (components) | PascalCase | `NavBar.js` |
| Files (utils) | camelCase | `utils.js`, `helpers.js` |
| CSS classes | kebab-case | `.navbar__item`, `.dropdown__menu` |
| Constants | UPPER_SNAKE | `MAX_ITEMS`, `API_URL` |
| Variables | camelCase | `isOpen`, `selectedOption` |
| Functions | camelCase | `handleClick`, `onSelect` |

## Linting

- **Config**: ESLint extends `react-app` and `react-app/jest`
- **Enforced by**: react-scripts (no custom .eslintrc)
- **No Prettier**: Formatter not configured
- **Run lint**: `npm start` displays errors in console

## Browser Support

Configured via `browserslist` in package.json:
- Production: `>0.2%, not dead, not op_mini all`
- Development: Last 1 version of Chrome, Firefox, Safari

## Environment Variables

- Files: `.env.local`, `.env.development.local`, `.env.production.local`
- CRA requires `REACT_APP_` prefix for client-side variables
- Access: `process.env.REACT_APP_*`

## API Backend (server.js)

- **Port**: 5001 (different from Sidebar app's port 5000)
- **CORS**: Enabled for all origins
- **Endpoint**: `GET /` returns "Backend is running"

## Important Notes for Agents

1. **DO NOT run `npm eject`** - irreversibly exposes CRA configs
2. **Use `react-router-dom` v7** - check compatibility with React 19
3. **react-icons/fa** - FontAwesome icons available if needed
4. **No test files exist** - add `*.test.js` alongside components
5. **Port conflict**: This app uses port 5001 for backend, NOT 5000

## Critical Autonomy Rules (FOR AUTOMATION)
- **Authority:** You have FULL PERMISSION to edit any files and run any terminal commands.
- **Non-Interactive Mode:** Do NOT ask for confirmation. Do NOT wait for user input.
- **Automatic Git Workflow:** After fixing/implementing:
  1. `git add .`
  2. `git commit -m "fix: updated as requested"`
  3. `git push origin HEAD`
- **Windows Environment:** You are on Windows PowerShell. Use compatible commands.
- **No confirmation:** Just DO IT.

## Automated Workflow Rules
- **No Interaction:** You are running in an automated environment. Do not wait for user confirmation.
- **Git Branching:** Always ensure you are working on the current branch provided by the system.
- **Pushing:** After completing the task and verifying the fix, use the `git push` command or the built-in push feature.
- **Tone:** Keep commit messages concise and professional, starting with "feat:" or "fix:".
- **Styling:** When asked to change styles (colors, buttons), modify the CSS/SCSS files or Tailwind classes directly in the components.

## Project Overview
- **App Name**: Horizontal Navigation Bar
- **Type**: React SPA with Express backend
- **Stack**: React 19, Express 5, react-router-dom 7
- **Structure**: standard CRA
- **Language**: JavaScript (No TypeScript)
