import React, { useState, useEffect } from 'react'
import { Routes, Route, Link } from "react-router-dom";
import Calendar from 'react-calendar'
import 'react-calendar/dist/Calendar.css';
import './App.css';
import Loginsignup from './components/Login/Login';
import Employees from './components/Employees/Employees'
import Store from './components/Store/Store'
import Holidays from './components/Holidays/Holidays'
import useToken from './useToken';

async function setAvailability(credentials) {
  return fetch('/api/setAvailability', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  }).then(res => res.json())
}

function App() {
  const { token, setToken } = useToken();

  console.log(token);

  if (!token) {
    return <Loginsignup setToken={setToken} />
  }

  return (
    <div>
      <nav>
        <Link to="/" id="home">OptiScheduler</Link>
        <Link to="/employees">Employees</Link>
        <Link to="/store">Store</Link>
        <Link to="/holidays">Holidays</Link>
        <Link to="/about">About</Link>
      </nav>
      <div className="wrapper">
        <Routes>
          <Route path="/" element={<Home token={token} />} />
          <Route path="about" element={<About />} />
          <Route path="employees/*" element={<Employees token={token} />} />
          <Route path="store/*" element={<Store token={token} />} />
          <Route path="holidays/*" element={<Holidays token={token} />} />
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
  const [warning, setWarning] = useState();
  const [refresh, setRefresh] = useState();

  useEffect(() => {
    fetch("/api/getAvailabilities", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        token,
        "day": date.getDay(),
        "date": date.toISOString()
      })
    }).then(res => res.json()
    ).then(
      data => {
        console.log(data);

        if (typeof data.error !== 'undefined') {
          if (data.error === 'Hours not yet set!') {
            setWarning("Store closed.");
          } else if(data.error === "Holiday") {
            setWarning("Closed for " + data.name);
          } else {
            alert(data.error);
          }
          setAvail([]);
        } else if (data["availability"].length === 0) {
          setWarning("No employees available.");
          setAvail([]);
        } else {
          setWarning("");
          setAvail(data["availability"]);
        }
      }
    )
  }, [token, date, refresh])

  function formatTime(time) {
    let hours = time.split(':')[0]
    let minutes = time.split(':')[1]

    let suffix = (hours >= 12) ? 'pm' : 'am';
    hours = (hours > 12) ? hours - 12 : hours;
    hours = (hours === '00') ? 12 : hours;

    return hours + ":" + minutes + suffix;
  }

  async function handleAdd(emp_id, day) {
    let err = await setAvailability({
      token,
      emp_id,
      day,
      is_scheduled: "True"
    })

    if (typeof err.error !== 'undefined') {
      alert(err.error);
    } else {
      console.log("test");
      setRefresh(emp_id + "True");
    }
  }

  async function handleRemove(emp_id, day) {
    let err = await setAvailability({
      token,
      emp_id,
      day,
      is_scheduled: "False"
    })

    if (typeof err.error !== 'undefined') {
      alert(err.error);
    } else {
      console.log("test");
      setRefresh(emp_id + "False");
    }
  }

  return (
    <>
      <main className="home-wrapper">
        <Calendar onChange={setDate} value={date} className="calendar" />
        <h2>Schedule</h2>
        {availabilities && availabilities.filter(availability => availability.isScheduled === 1).map(data => (
          <div key={data.id} className="employee">
            <div className="name">{data.first_name} {data.last_name}</div>
            <div className="left">
              <button className="add" onClick={() => { handleRemove(data.Employee_id, data.day) }}>-</button>
              <div className="time">
                <div className="start">
                  {formatTime(data.start_time)} -
                </div>
                <div className="end">
                  {formatTime(data.end_time)}
                </div>
              </div>
            </div>
          </div>
        ))}
        {warning ? <h3>{warning}</h3> : <h3>Available Employees</h3>}
        {availabilities && availabilities.filter(availability => availability.isScheduled === 0).map(data => (
          <div key={data.id} className="employee">
            <div className="name">{data.first_name} {data.last_name}</div>
            <div className="left">
              <button className="add" onClick={() => { handleAdd(data.Employee_id, data.day) }}>+</button>
              <div className="time">
                <div className="start">
                  {formatTime(data.start_time)} -
                </div>
                <div className="end">
                  {formatTime(data.end_time)}
                </div>
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