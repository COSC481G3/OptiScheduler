import React, { useState, useEffect } from 'react'
import { Routes, Route, Link } from "react-router-dom";

function App() {

  return (
    <div>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="about" element={<About />} />
      </Routes>

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
        <h2>Welcome to the homepage!</h2>
        <p>Here's some data retrieved from the backend:</p>
        <><p>{data.name}</p><p>{data.response}</p></>
      </main>
      <nav>
        <Link to="/about">About</Link>
      </nav>
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
      <nav>
        <Link to="/">Home</Link>
      </nav>
    </>
  )
}

export default App