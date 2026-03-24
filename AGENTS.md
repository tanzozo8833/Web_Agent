# AGENTS.md - Codebase Guide

This document provides guidance for AI agents operating in this repository.

## Project Overview

- **Type**: React SPA with Express backend
- **Stack**: React 19, Express 5, react-router-dom 7
- **Structure**: CRA (Create React App) - ejected configuration NOT used
- **Language**: JavaScript (no TypeScript)

## Project Structure

```
├── public/           # Static assets (HTML, icons, manifest)
├── src/
│   ├── components/   # React components
│   ├── App.js        # Main app component
│   ├── App.css       # App-specific styles
│   ├── index.js      # Entry point
│   └── index.css     # Global styles
├── server.js         # Express backend (port 5000)
└── package.json
```

## Build/Lint/Test Commands

```bash
# Development
npm start              # Start React dev server (port 3000)
node server.js         # Start Express backend (port 5000)

# Production
npm run build          # Build optimized bundle to /build

# Testing (Jest + React Testing Library)
npm test               # Run tests in watch mode
npm test -- --watchAll=false           # Run tests once (CI mode)
npm test -- --testPathPattern=Home     # Run single test file matching "Home"
npm test -- --testNamePattern="renders" # Run tests with name containing "renders"
npm test -- --coverage                  # Generate coverage report
```

### Testing Setup

- **Framework**: Jest (via react-scripts)
- **Libraries**: @testing-library/react, @testing-library/user-event, @testing-library/jest-dom
- **Test file pattern**: `*.test.js` or `*.spec.js` (place alongside source files)
- **Example test structure**:
  ```javascript
  import { render, screen } from '@testing-library/react';
  import userEvent from '@testing-library/user-event';
  import Home from './Home';

  test('renders heading', () => {
    render(<Home />);
    expect(screen.getByRole('heading', { name: /home page/i })).toBeInTheDocument();
  });
  ```

## Code Style Guidelines

### JavaScript Conventions

1. **File naming**: PascalCase for components (`Home.js`), camelCase for utilities
2. **Component naming**: Use PascalCase, match filename
3. **Imports**: Use double quotes for consistency with CRA defaults
4. **Prop destructuring**: Prefer in function parameters
5. **No TypeScript**: Plain JavaScript only

### React Patterns

```javascript
// ✅ Preferred: functional components with arrow functions
const Home = () => {
  return <div>Content</div>;
};

// ✅ Preferred: named exports + default export
export const Home = () => { ... };
export default Home;

// ✅ Preferred: inline styles use double quotes
<div style={{ display: "flex" }}>

// ❌ Avoid: inline arrow functions in JSX (extract to named functions)
```

### CSS Conventions

1. **BEM-lite**: Use lowercase with hyphens (`.sidebar`, `.sidebar-item`)
2. **Component CSS**: Co-locate with component (e.g., `Sidebar.css` with `Sidebar.js`)
3. **CSS files**: camelCase naming (`App.css`, `index.css`)
4. **Classes**: BEM-style (`.sidebar__item`, `.sidebar--active`)
5. **Inline styles**: Use double quotes, camelCase properties

### Import Conventions

```javascript
// ✅ React core
import React from "react";

// ✅ Components (relative paths)
import Sidebar from "./components/Sidebar";

// ✅ Icons (named imports from react-icons/fa)
import { FaHome, FaUser } from "react-icons/fa";

// ✅ CSS (co-located or global)
import "./Sidebar.css";
import "./index.css";
```

### Error Handling

```javascript
// ✅ Express backend error handling
app.get("/", (req, res) => {
  try {
    // logic
    res.json({ data });
  } catch (error) {
    console.error("Error:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `HomePage`, `UserDashboard` |
| Files (components) | PascalCase | `HomePage.js` |
| Files (utils) | camelCase | `utils.js`, `helpers.js` |
| CSS classes | kebab-case | `.sidebar-nav`, `.nav-item` |
| Constants | UPPER_SNAKE | `MAX_RETRIES`, `API_URL` |
| Variables | camelCase | `userName`, `isLoading` |
| Functions | camelCase | `handleClick`, `fetchData` |

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

- **Port**: 5000
- **CORS**: Enabled for all origins
- **Endpoint**: `GET /` returns "Backend is running"

## Important Notes for Agents

1. **DO NOT run `npm eject`** - irreversibly exposes CRA configs
2. **Use `react-router-dom` v7** - check compatibility with React 19
3. **react-icons/fa** - FontAwesome icons are in use
4. **No test files exist** - add `*.test.js` alongside components
5. **CSS files exist**: `App.css`, `index.css`, `Sidebar.css`
