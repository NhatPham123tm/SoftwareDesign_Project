import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import './SignUp.css';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api',
  withCredentials: true, // send session cookies
});

export default function Signup() {
  const [id, setId] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [retypePassword, setRetypePassword] = useState('');
  const [microsoftAuth, setMicrosoftAuth] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSignup = async () => {
    setError('');

    if (!id || !password || !retypePassword) {
      setError('Please fill in UH ID and password fields.');
      return;
    }
    if (password !== retypePassword) {
      setError('Passwords do not match.');
      return;
    }

    if (!microsoftAuth && (!name || !email)) {
      setError('Please fill in all required fields.');
      return;
    }

    // Set cookies for Microsoft Auth fallback
    document.cookie = `sessionId=${id}; path=/; max-age=${60}`;
    document.cookie = `password=${password}; path=/; max-age=${60}`;

    if (microsoftAuth) {
      window.location.href = '/login/microsoft/';
      return;
    }

    try {
      const res = await axiosInstance.post('/user_register/', {
        id,
        password,
        name,
        email,
      }, {
        headers: {
          'X-CSRFToken': getCSRFToken(),
        },
      });

      if (res.data?.message === 'User registered successfully!') {
        alert('Account created! Please log in.');
        navigate('/login');
      } else {
        setError(res.data?.message || 'Registration failed.');
      }
    } catch (err) {
      console.error(err);
      const errorMsg = err.response?.data?.message || 'An error occurred.';
      setError(errorMsg);
    }
  };

  const getCSRFToken = () => {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : null;
  };

  return (
    <div className="signup-container">
      <div className="signup-box">
        <h2>Create Account</h2>
        <p>Sign up to get started</p>

        {error && <div className="error-message">{error}</div>}

        <input
          value={id}
          onChange={e => setId(e.target.value)}
          placeholder="UH ID (7 digits)"
          className="input-field"
          required
        />
        <input
          value={password}
          onChange={e => setPassword(e.target.value)}
          placeholder="Password (min 7 characters)"
          className="input-field"
          type="password"
          minLength={7}
          required
        />
        <input
          value={retypePassword}
          onChange={e => setRetypePassword(e.target.value)}
          placeholder="Confirm Password"
          className="input-field"
          type="password"
          required
        />
        <input
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="Full Name"
          className="input-field"
          disabled={microsoftAuth}
          required={!microsoftAuth}
        />
        <input
          value={email}
          onChange={e => setEmail(e.target.value)}
          placeholder="Email"
          className="input-field"
          type="email"
          disabled={microsoftAuth}
          required={!microsoftAuth}
        />

        <div className="checkbox-row">
          <input
            type="checkbox"
            id="microsoftAuth"
            checked={microsoftAuth}
            onChange={() => setMicrosoftAuth(!microsoftAuth)}
          />
          <label htmlFor="microsoftAuth">Link with Microsoft</label>
        </div>

        <button className="signup-button" onClick={handleSignup}>
          {microsoftAuth ? 'Continue with Microsoft' : 'Sign Up'}
        </button>

        <p className="login-text">
          Already have an account? <Link to="/" className="login-link">Log In</Link>
        </p>
      </div>
    </div>
  );
}
