import { useRef, useState, type FormEvent } from 'react';
import './Login.css';

type LoginProps = {
  onLogin: (username: string) => void;
};

export default function Login({ onLogin }: LoginProps) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const submitInFlightRef = useRef(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (submitInFlightRef.current) {
      return;
    }

    setError(null);
    const normalizedUsername = username.trim();

    if (!normalizedUsername || !password) {
      setError('Please enter both username and password.');
      return;
    }

    submitInFlightRef.current = true;
    setLoading(true);

    try {
      // Simulate an async login call. Replace with a real API call.
      await new Promise((r) => setTimeout(r, 600));
      onLogin(normalizedUsername);
    } catch (error) {
      console.error('Sign in failed.', error);
      setError('Unable to sign in right now. Please try again.');
    } finally {
      submitInFlightRef.current = false;
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <form className="login-card" onSubmit={handleSubmit} noValidate>
        <h1 className="login-title">Sign In</h1>
        <p className="login-subtitle">
          Welcome back! Demo mode signs you in locally with any non-empty credentials.
        </p>

        <label className="login-label" htmlFor="username">
          Username
        </label>
        <input
          id="username"
          className="login-input"
          type="text"
          autoComplete="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="admin"
        />

        <label className="login-label" htmlFor="password">
          Password
        </label>
        <div className="login-password-wrapper">
          <input
            id="password"
            className="login-input"
            type={showPassword ? 'text' : 'password'}
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
          />
          <button
            type="button"
            className="login-toggle"
            onClick={() => setShowPassword((s) => !s)}
            aria-label={showPassword ? 'Hide password' : 'Show password'}
          >
            {showPassword ? 'Hide' : 'Show'}
          </button>
        </div>

        {error && <div className="login-error">{error}</div>}

        <button type="submit" className="login-button" disabled={loading}>
          {loading ? 'Signing in…' : 'Sign In'}
        </button>

        <p className="login-hint">Your username is trimmed before sign-in.</p>
      </form>
    </div>
  );
}
