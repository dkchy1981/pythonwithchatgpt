import { useState } from 'react';
import Login from './Login';
import './App.css';

function App() {
  const [user, setUser] = useState<string | null>(null);

  if (!user) {
    return <Login onLogin={setUser} />;
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>Welcome, {user} 👋</h1>
        <button className="logout-button" onClick={() => setUser(null)}>
          Log out
        </button>
      </header>
      <main className="app-main">
        <p>You are now signed in. This is your protected content area.</p>
      </main>
    </div>
  );
}

export default App;
