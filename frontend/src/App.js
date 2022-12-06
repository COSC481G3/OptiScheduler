import React, { useState, useEffect } from 'react'
import { Routes, Route, Link, useNavigate, useLocation } from "react-router-dom";
import Calendar from 'react-calendar'
import 'react-calendar/dist/Calendar.css';
import './App.css';
import Loginsignup from './components/Login/Login';
import Employees from './components/Employees/Employees'
import Store from './components/Store/Store'
import Holidays from './components/Holidays/Holidays'
import useToken from './useToken';

async function addSchedule(credentials) {
  return fetch('/api/addSchedule', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  }).then(res => res.json())
}

async function deleteSchedule(credentials) {
  return fetch('/api/deleteSchedule', {
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
          <Route path="schedule/*" element={<ScheduleDetails token={token} />} />
        </Routes>
      </div>
    </div>
  )
}

// Home
function Home({ token }) {
  let location = useLocation();
  var ddate = new Date();

  if(location.state){
    let olddate = location.state.date.split("T")[0];
    console.log(olddate);
    ddate.setFullYear(olddate.split("-")[0], olddate.split("-")[1]-1, olddate.split("-")[2]);
  }

  const [date, setDate] = useState(ddate)
  const [availabilities, setAvail] = useState([]);
  const [schedule, setSchedule] = useState([]);
  const [warning, setWarning] = useState();
  const [refresh, setRefresh] = useState();

  useEffect(() => {
    async function fetchAPI() {
      await fetch("/api/getAvailabilities", {
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
            } else if (data.error === "Holiday") {
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

      await fetch("/api/getSchedules", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          token,
          "date": date.toISOString()
        })
      }).then(res => res.json()
      ).then(
        data => {
          console.log(data);

          if (typeof data.error !== 'undefined') {
            alert(data.error)
          } else {
            setSchedule(data["schedules"]);
          }
        }
      )
    }

    fetchAPI();
  }, [token, date, refresh])

  function formatTime(time) {
    let hours = time.split(':')[0]
    let minutes = time.split(':')[1]

    let suffix = (hours >= 12) ? 'pm' : 'am';
    hours = (hours > 12) ? hours - 12 : hours;
    hours = (hours === '00') ? 12 : hours;

    return hours + ":" + minutes + suffix;
  }

  async function handleRemove(emp_id) {
    let err = await deleteSchedule({
      token,
      emp_id,
      "date": date.toISOString()
    })

    if (typeof err.error !== 'undefined') {
      alert(err.error);
    } else {
      console.log("test");
      setRefresh(emp_id + "False" + date.toISOString());
    }
  }

  return (
    <>
      <main className="home-wrapper">
        <Calendar onChange={setDate} value={date} className="calendar" />
        <h2>Schedule</h2>
        {schedule.map(data => (
          <div key={data.id} className="employee">
            <div className="name">{data.first_name} {data.last_name}</div>
            <div className="left">
              <button className="add" onClick={() => { handleRemove(data.employee_id) }}>-</button>
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
        {availabilities.map(data => (
          <div key={data.id} className="employee">
            <div className="name">{data.first_name} {data.last_name}</div>
            <div className="left">
              <Link to="/schedule" className="add" state={{ data, "date": date.toISOString() }}>+</Link>
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

function ScheduleDetails({ token }) {
  const [first_name, setFirstName] = useState();
  const [last_name, setLastName] = useState();
  const [start_time, setStartTime] = useState();
  const [end_time, setEndTime] = useState();
  const [date, setDate] = useState("");
  const [emp_id, setEmpID] = useState();
  let navigate = useNavigate();
  let location = useLocation();

  useEffect(() => {
    if (location.state) {
      let data = location.state.data;
      let date = location.state.date;
      console.log(data);
      console.log(date);

      setFirstName(data.first_name);
      setLastName(data.last_name);
      if (data.start_time.length === 7) {
        data.start_time = "0" + data.start_time;
      }
      if (data.end_time.length === 7) {
        data.end_time = "0" + data.end_time;
      }
      setStartTime(data.start_time);
      setEndTime(data.end_time);
      setEmpID(data.Employee_id);
      setDate(date);
    }
  }, [location.state])

  const handleSubmit = async e => {
    e.preventDefault();

    let err = await addSchedule({
      token,
      emp_id,
      date,
      start_time,
      end_time
    });

    if (typeof err.error !== 'undefined') {
      alert(err.error)
    } else {
      navigate("/", { state: { date }});
    }
  }

  return (
    <>
      <main className="sch-wrapper">
        <form onSubmit={handleSubmit}>
          <h3>{first_name} {last_name}</h3>
          <h3>{date.split("T")[0]}</h3>
          <label>
            Start
          </label>
          <input type="time" value={start_time} min={start_time} max={end_time} onChange={e => setStartTime(e.target.value)}></input>
          <label>
            End
          </label>
          <input type="time" value={end_time} min={start_time} max={end_time} onChange={e => setEndTime(e.target.value)}></input>
          <button type="submit" id="submit">Submit</button>
        </form>
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