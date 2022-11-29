import React, { useState, useEffect } from 'react'
import { Routes, Route, Link } from "react-router-dom";
import Calendar from 'react-calendar'
import 'react-calendar/dist/Calendar.css';
import './App.css';
import Loginsignup from './components/Login/Login';
import Employees from './components/Employees/Employees'
import Store from './components/Store/Store'


function App() {
  const [token, setToken] = useState();

  if (!token) {
    return <Loginsignup setToken={setToken} />
  }

  return (
    <div>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/employees">Employees</Link>
        <Link to="/store">Store</Link>
        <Link to="/about">About</Link>
      </nav>
      <div className="wrapper">
        <Routes>
          <Route path="/" element={<Home token={token} />} />
          <Route path="about" element={<About />} />
          <Route path="employees/*" element={<Employees token={token} />} />
          <Route path="store/*" element={<Store token={token} />} />
        </Routes>
      </div>
    </div>
  )
}

// Home
function Home({ token }) {

  //Gets data from /api/hello endpoint, sets it to data variable.
  const [date, setDate] = useState(new Date())
  const [availabilities, setAvail] = useState([]);

  useEffect(() => {
    fetch("/api/getSchedule", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        token,
        "day": date.getDay()
      })
    }).then(res => res.json()
    ).then(
      data => {
        console.log(data);

        if (typeof data.error !== 'undefined') {
          console.log(data.error);
        } else {
          setAvail(data["availability"]);
        }
      }
    )
  }, [token, date])

  function formatTime(time) {
    let hours = time.split(':')[0]
    let minutes = time.split(':')[1]

    let suffix = (hours >= 12) ? 'pm' : 'am';
    hours = (hours > 12) ? hours - 12 : hours;
    hours = (hours === '00') ? 12 : hours;

    return hours + ":" + minutes + suffix;
  }

  return (
    <>
      <main id="home">
        <Calendar onChange={setDate} value={date} className="calendar" />
        <h2>Schedule</h2>
        {availabilities.map(data => (
          <div key={data.id} className="employee">
            <div className="name">{data.first_name} {data.last_name}</div>
            <div className="left">
              <div className="start">
                {formatTime(data.start_time)} -
              </div>
              <div className="end">
                {formatTime(data.end_time)}
              </div>
            </div>
          </div>
        ))}
      </main>
    </>
  )
}

// About
function About() {
  return (
    <>
      <main id="about">
        <h2>Who are we?</h2>
        <p>We are group 3!</p>
      </main>
    </>
  )
}

export default App