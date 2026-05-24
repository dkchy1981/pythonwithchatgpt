# React + TypeScript Coding Standards

## Objective

Ensure React applications are scalable, maintainable, type-safe, and follow consistent development practices.

All generated code must follow these standards.

---

# Technology Standards

Required:

- React Functional Components
- TypeScript Strict Mode
- Hooks-based architecture
- Strong typing
- Modular folder structure
- Reusable components
- Separation of concerns

Avoid:

- Class components
- `any` type
- Inline business logic
- Large components
- Duplicated code

---

# Project Structure

Organize code by responsibility.

Example:

src/
├── components/
├── pages/
├── hooks/
├── services/
├── types/
├── models/
├── utils/
├── context/
├── constants/
├── api/
├── routes/
├── assets/
├── styles/
└── tests/

Rules:

- Components only contain UI logic
- API calls belong in services
- Types belong in types folder
- Constants belong in constants folder
- Shared utilities belong in utils

---

# File Naming Standards

Components:

```text
UserCard.tsx
LoginForm.tsx
```

Hooks:

```text
useAuth.ts
useUserData.ts
```

Services:

```text
userService.ts
authService.ts
```

Types:

```text
userTypes.ts
apiTypes.ts
```

Utilities:

```text
dateUtils.ts
validationUtils.ts
```

Naming:

- PascalCase → Components
- camelCase → Variables
- camelCase → Functions
- UPPER_SNAKE_CASE → Constants
- Interfaces → PascalCase
- Types → PascalCase

---

# Component Standards

Prefer:

```tsx
interface UserCardProps {
    name: string;
}

const UserCard = ({
    name
}: UserCardProps): JSX.Element => {

    return (
        <div>{name}</div>
    );

};

export default UserCard;
```

Rules:

- Use functional components only
- Always define Props interfaces
- Keep components focused on single responsibility
- Prefer explicit return types

Avoid:

```tsx
const UserCard = (props:any) => {}
```

---

# TypeScript Standards

Never use:

```typescript
any
```

Incorrect:

```typescript
const data:any = response;
```

Correct:

```typescript
interface User {
    id: number;
    name: string;
}

const data: User = response;
```

Prefer:

```typescript
type Status =
    "Active"
    | "Inactive";
```

Use interface for object contracts:

```typescript
interface User {

    id: number;

    name: string;

    email?: string;

}
```

---

# State Management

Always strongly type state.

Correct:

```typescript
const [
    users,
    setUsers
] = useState<User[]>([]);
```

Boolean state:

```typescript
const [
    loading,
    setLoading
] = useState<boolean>(false);
```

Nullable:

```typescript
const [
    selectedUser,
    setSelectedUser
] =
useState<User | null>(
    null
);
```

Avoid:

```typescript
useState([])
```

---

# Props Standards

Always define props interface.

Correct:

```tsx
interface ButtonProps {

    label: string;

    disabled?: boolean;

    onClick: () => void;

}
```

Avoid:

```tsx
(props:any)
```

---

# API Layer Standards

Never place API calls inside components.

Incorrect:

```typescript
axios.get("/users")
```

Correct:

services/userService.ts

```typescript
import api from "../api/client";

import {
    User
} from "../types/userTypes";

export const getUsers =
async (): Promise<User[]> => {

    const response =
        await api.get<User[]>(
            "/users"
        );

    return response.data;

};
```

---

# Exception Handling

All async operations require:

```typescript
try {

}
catch(error){

}
finally{

}
```

Example:

```typescript
try {

    const users =
      await getUsers();

    setUsers(users);

}
catch(error){

    setError(
      "Unable to load users"
    );

}
finally{

    setLoading(false);

}
```

Never swallow exceptions.

---

# Hooks Standards

Correct:

```typescript
const useUsers = () => {

    const [
        users,
        setUsers
    ] = useState<User[]>([]);

    return {
        users
    };

};
```

Rules:

- Hooks start with "use"
- Hooks cannot be conditional
- Keep hooks reusable

---

# useEffect Standards

Correct:

```typescript
useEffect(() => {

    loadUsers();

}, []);
```

Always specify dependencies.

Avoid large useEffect blocks.

---

# Constants

Avoid magic numbers.

Incorrect:

```typescript
if(status === 1)
```

Correct:

```typescript
export const STATUS_ACTIVE =
    1;
```

---

# Utility Functions

Move reusable logic:

Incorrect:

```typescript
const age =
today-year;
```

Correct:

```typescript
calculateAge()
```

---

# Imports

Import order:

1 React

2 External libraries

3 Components

4 Hooks

5 Services

6 Types

7 Utils

8 Styles

Example:

```typescript
import React from "react";

import axios from "axios";

import UserCard
from "../components/UserCard";

import {
    User
}
from "../types/userTypes";

import "./UserPage.css";
```

---

# Performance

Use:

```typescript
useMemo()
```

```typescript
useCallback()
```

```typescript
React.memo()
```

Only when necessary.

---

# Accessibility

Always include:

```tsx
aria-label
```

```tsx
alt
```

Example:

```tsx
<button
 aria-label="Save User"
>
Save
</button>
```

---

# Security

Never:

- Store secrets in code
- Store tokens in localStorage when avoidable
- Trust client validation alone
- Expose stack traces

Environment variables:

```text
VITE_API_URL
```

or

```text
REACT_APP_API_URL
```

---

# Logging

Development:

```typescript
console.error()
```

Production:

Use centralized logging.

Remove:

```typescript
console.log()
```

before release.

---

# Testing Standards

Test:

- Rendering
- State updates
- API failures
- Validation
- Loading states

Preferred:

- Jest
- React Testing Library

---

# Documentation Standards

Complex code requires:

```typescript
/**
 * Retrieves users from API.
 *
 * @returns User collection
 */
```

Public utilities require documentation.

---

# Copilot Rules

Generated code must:

- Use TypeScript strict typing
- Avoid any
- Use interfaces
- Use reusable components
- Separate API layer
- Include loading states
- Include exception handling
- Follow naming conventions
- Avoid duplicated code
- Use functional components only

Goal:

Code must be scalable, maintainable, type-safe, and production ready.