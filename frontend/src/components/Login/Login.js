import React, { useState } from 'react';
import { Routes, Route, Link } from "react-router-dom";
import PropTypes from 'prop-types';
import './Login.css'

async function loginUser(credentials) {
    return fetch('/api/getToken', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(res => res.json())
}

async function signupUser(credentials) {
    return fetch('/api/addUser', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(res => res.json())
}

export default function Loginsignup({ setToken }) {
    return (
        <div className="wrapper">
            <Routes>
                <Route path="/" element={<Login setToken={setToken} />} />
                <Route path="signup" element={<SignUp />} />
            </Routes>
        </div>
    )
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired
}

function Login({ setToken }) {
    const [username, setUserName] = useState();
    const [password, setPassword] = useState();

    const handleSubmit = async e => {
        e.preventDefault();
        const token = await loginUser({
            username,
            password
        });

        if (typeof token.error !== 'undefined') {
            alert(token.error)
        } else if (token.token !== 'undefined') {
            setToken(token.token);
        }
    }

    return (
        <div className="login-wrapper">
            <div className="login-div">
                <form onSubmit={handleSubmit}>
                    <h3>Sign In</h3>
                    <label>
                        Username
                    </label>
                    <input type="text" placeholder="Email or Username" onChange={e => setUserName(e.target.value)} />
                    <label>
                        Password
                    </label>
                    <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
                    <button type="submit" id="submit">Submit</button>
                    <Link className="altbutton" to="/signup">Sign Up</Link>
                </form>
            </div>
        </div>
    )
}

function SignUp() {
    const [username, setUserName] = useState();
    const [password, setPassword] = useState();
    const [password2, setPassword2] = useState();

    const handleSubmit = async e => {
        e.preventDefault();

        if (password !== password2){
            alert("Passwords must match!");
            return;
        }

        const token = await signupUser({
            username,
            password
        });

        if (typeof token.error !== 'undefined') {
            alert(token.error)
        } else {
            alert("Success! Please sign in.")
        }
    }

    return (
        <div className="login-wrapper">
            <div className="login-div">
                <form onSubmit={handleSubmit}>
                    <h3>Sign Up</h3>
                    <label>
                        Username
                    </label>
                    <input type="text" placeholder="Email or Username" onChange={e => setUserName(e.target.value)} />
                    <label>
                        Password
                    </label>
                    <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
                    <input type="password" placeholder="Confirm Password" onChange={e => setPassword2(e.target.value)} />
                    <button type="submit" id="submit">Submit</button>
                    <Link className="altbutton" to="/">Sign In</Link>
                </form>
            </div>
        </div>
    )
}