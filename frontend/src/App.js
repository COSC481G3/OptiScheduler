import React, { useState, useEffect } from 'react'
// import { Routes, Route, Link } from "react-router-dom";
import './App.css';
import Loginsignup from './components/Login/Login';
import Employees from './components/Employees/Employees'
import Sidebar from './components/Sidebar';
// import '././node_modules/node_modules/bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import { BrowserRouter as Router, Route, Switch, Routes, Link } from "react-router-dom";
import { NavigationBar } from './components/NavigationBar';
import Store from './components/Store/Store'
function App() {
  const [token, setToken] = useState();

  if (!token) {
    return <Loginsignup setToken={setToken} />
  }

  return (
    <div>
      {/* <nav>
        <Link to="/">Home</Link>
        <Link to="/employees">Employees</Link>
        <Link to="/store">Store</Link>
        <Link to="/about">About</Link>
      </nav>
      <div className="wrapper">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="about" element={<About />} />
          <Route path="employees/*" element={<Employees token={token} />} />
          <Route path="store" element={<Store token={token} />} />
        </Routes>
      </div> */}

      <React.Fragment>
        <Router>
          <NavigationBar />
        </Router>
      </React.Fragment>
    </div>
  )
}

// Home
function Home() {

  //Gets data from /api/hello endpoint, sets it to data variable.
  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/api/hello").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])

  return (
    <>
      <main>
        <h2>Welcome to the homepage friend! :)</h2>
        <p>Here's some data retrieved from the backend:</p>
        <><p>{data.name}</p><p>{data.response}</p></>
        <Sidebar />
      </main>
    </>
  )
}

// About
function About() {
  return (
    <>
      <main>
        <h2>Who are we?</h2>
        <p>We are group 3!</p>
      </main>
    </>
  )
}

export default App