# React Login App

A React + TypeScript login flow demo created with Vite.

## Tech Stack

- React 19
- TypeScript
- Vite
- ESLint

## Available Scripts

From `react-login-app`:

```bash
npm run dev
```

Runs the Vite development server.

```bash
npm run build
```

Compiles TypeScript and creates a production build.

```bash
npm run preview
```

Previews the production build locally.

```bash
npm run lint
```

Runs ESLint checks.

## Current Behavior

- Shows a login form with:
	- Username field
	- Password field
	- Show/Hide password toggle
	- Inline validation and error messaging
	- Loading state during simulated async sign-in
- Uses demo credentials:
	- Username: `admin`
	- Password: `password123`
- On successful sign-in:
	- Displays a welcome screen (`Welcome, {user}`)
	- Shows a protected content placeholder
	- Provides a logout button that returns to login view

## Styling Notes

- `src/Login.css` styles the login experience using a gradient background and centered card.
- `src/App.css` styles the signed-in shell and logout experience.
- `src/index.css` still includes broader Vite starter root-level styles.

## Recent Changes

1. Added a functional login flow in `src/Login.tsx` with form state, validation, loading simulation, and credential checks.
2. Connected authentication state in `src/App.tsx` to toggle between login and signed-in views.
3. Added dedicated styles for login and app shell in `src/Login.css` and `src/App.css`.
4. Added logout support by resetting user state.

## Documentation Maintenance (For Future Changes)

Update this README whenever project behavior changes.

Must-update triggers:

- Authentication logic changes (API integration, token storage, route protection)
- Credential policy changes (demo credentials removed/changed)
- Script changes in `package.json`
- UX or validation flow changes
- Dependency or tooling upgrades that affect usage

Required update checklist:

1. Update `Current Behavior` with the exact runtime behavior.
2. Update `Available Scripts` if command behavior changes.
3. Add a new entry to `Recent Changes`.
4. Adjust setup instructions if dependencies or requirements change.
5. Keep entries factual and based on code currently in the repository.

## Known Limitations

- Authentication is client-side only and not secure for production.
- Login request is simulated (`setTimeout`) and not connected to a backend API.
