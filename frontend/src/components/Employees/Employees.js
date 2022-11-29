import React, { useState, useEffect } from 'react';
import { Routes, Route, Link, useNavigate, useLocation } from "react-router-dom";
import './Employees.css'

async function addEmployee(credentials) {
    return fetch('/api/addEmployee', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(res => res.json())
}

async function setEmployee(credentials) {
    return fetch('/api/setEmployee', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(res => res.json())
}

async function deleteEmployee(credentials) {
    return fetch('/api/deleteEmployee', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(res => res.json())
}

async function addAvailability(credentials) {
    return fetch('/api/addAvailability', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(res => res.json())
}

export default function Employees({ token }) {
    return (
        <div className="emp-wrapper">
            <nav>
                <Link to="/employees">List All Employees</Link>
                <Link to="/employees/employee">Add Employee</Link>
            </nav>
            <Routes>
                <Route path="/" element={<ListEmployees token={token} />} />
                <Route path="/employee" element={<EmployeeDetails token={token} />} />
                <Route path="/availability" element={<EmployeeAvailability token={token} />} />
            </Routes>
        </div>
    )
}

function ListEmployees({ token }) {
    const [employees, setEmployees] = useState();
    const [search, setSearch] = useState();
    const [refresh, setRefresh] = useState();

    useEffect(() => {
        fetch("/api/getEmployees", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token
            })
        }).then(res => res.json()
        ).then(
            data => {
                setEmployees(data["employees"]);
                console.log("list");
                console.log(data);
            }
        )

        setSearch("");

    }, [token, refresh])

    async function handleClick(emp_id) {
        let err = await deleteEmployee({
            token,
            emp_id
        })

        if (typeof err.error !== 'undefined') {
            alert(err.error);
        } else {
            setRefresh(emp_id);
        }
    }

    return (
        <>
            <main id="employee">
                <h2>Employees</h2>
                <input type="text" placeholder="Search" className="search" onChange={e => setSearch(e.target.value)}></input>
                {employees && employees.filter(employee => employee.first_name.includes(search) || employee.last_name.includes(search)).map(data => (
                    <div key={data.id} className="employee">
                        <div className="name">{data.first_name} {data.last_name}</div>
                        <div className="dob">DOB: <b>{data.DOB}</b></div>
                        <div className="pto">PTO: <b>{data.PTO_Days_Rem}</b></div>
                        <div className="left">
                            <Link to="/employees/availability" className="addemployee" state={{ data }}>Availability</Link>
                            <Link to="/employees/employee" className="addemployee" state={{ data }}>Edit</Link>
                            <button className="addemployee" onClick={() => { handleClick(data.id) }}>Delete</button>
                        </div>
                    </div>
                ))}
            </main>
        </>
    )
}

function EmployeeDetails({ token }) {
    const [first_name, setFirstName] = useState();
    const [last_name, setLastName] = useState();
    const [emp_id, setEmpID] = useState();
    const [DOB, setDob] = useState();
    const [PTO_Days_Rem, setPto] = useState();
    let navigate = useNavigate();
    let location = useLocation();

    useEffect(() => {
        if (location.state) {
            let data = location.state.data;
            console.log("Details");
            console.log(data);
            setFirstName(data.first_name);
            setLastName(data.last_name);
            setEmpID(data.id);
            setDob(data.DOB);
            setPto(data.PTO_Days_Rem);
        }
    }, [location.state])

    const handleSubmit = async e => {
        e.preventDefault();
        let err;

        if (emp_id) {
            err = await setEmployee({
                first_name,
                last_name,
                DOB,
                PTO_Days_Rem,
                token,
                emp_id
            });
        } else {
            err = await addEmployee({
                first_name,
                last_name,
                DOB,
                PTO_Days_Rem,
                token
            });
        }

        if (typeof err.error !== 'undefined') {
            alert(err.error)
        } else {
            navigate("/employees");
        }
    }

    return (
        <>
            <main>
                <form onSubmit={handleSubmit}>
                    <h3>Employee</h3>
                    <label>
                        First name
                    </label>
                    <input type="text" placeholder="First Name" value={first_name} onChange={e => setFirstName(e.target.value)} />
                    <label>
                        Last name
                    </label>
                    <input type="text" placeholder="Last Name" value={last_name} onChange={e => setLastName(e.target.value)} />
                    <label>
                        Date of Birth
                    </label>
                    <input type="date" value={DOB} onChange={e => setDob(e.target.value)} />
                    <label>
                        PTO Days
                    </label>
                    <input type="number" placeholder="Number" value={PTO_Days_Rem} onChange={e => setPto(e.target.value)} />
                    <button type="submit" id="submit">Submit</button>
                </form>
            </main>
        </>
    )
}

function EmployeeAvailability({ token }) {
    const [first_name, setFirstName] = useState();
    const [last_name, setLastName] = useState();
    const [emp_id, setEmpID] = useState();

    const [monStart, setMonStart] = useState();
    const [monEnd, setMonEnd] = useState();
    const [tueStart, setTueStart] = useState();
    const [tueEnd, setTueEnd] = useState();
    const [wedStart, setWedStart] = useState();
    const [wedEnd, setWedEnd] = useState();
    const [thuStart, setThuStart] = useState();
    const [thuEnd, setThuEnd] = useState();
    const [friStart, setFriStart] = useState();
    const [friEnd, setFriEnd] = useState();
    const [satStart, setSatStart] = useState();
    const [satEnd, setSatEnd] = useState();
    const [sunStart, setSunStart] = useState();
    const [sunEnd, setSunEnd] = useState();

    let navigate = useNavigate();
    let location = useLocation();

    useEffect(() => {
        if (location.state) {
            let data = location.state.data;
            console.log("Availability");
            console.log(data);
            setFirstName(data.first_name);
            setLastName(data.last_name);
            setEmpID(data.id);

            fetch("/api/getAvailability", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    token,
                    "emp_id": data.id
                })
            }).then(res => res.json()
            ).then(
                data => {
                    let availability = data["availability"];
                    console.log(availability);
                    availability.forEach((day) => {
                        if(day.start_time.length === 7){
                            day.start_time = "0" + day.start_time;
                        }
                        if(day.end_time.length === 7){
                            day.end_time = "0" + day.end_time;
                        }

                        if(day.day === "Monday"){
                            setMonStart(day.start_time);
                            setMonEnd(day.end_time);
                        } else if(day.day === "Tuesday"){
                            setTueStart(day.start_time);
                            setTueEnd(day.end_time);
                        } else if(day.day === "Wednesday"){
                            setWedStart(day.start_time);
                            setWedEnd(day.end_time);
                        } else if(day.day === "Thursday"){
                            setThuStart(day.start_time);
                            setThuEnd(day.end_time);
                        } else if(day.day === "Friday"){
                            setFriStart(day.start_time);
                            setFriEnd(day.end_time);
                        } else if(day.day === "Saturday"){
                            setSatStart(day.start_time);
                            setSatEnd(day.end_time);
                        } else if(day.day === "Sunday"){
                            setSunStart(day.start_time);
                            setSunEnd(day.end_time);
                        }

                        console.log(day);
                    });
                }
            )
        }
    }, [location.state, token])

    const handleSubmit = async e => {
        e.preventDefault();
        let err;

        if (monStart && monEnd) {
            err = await addAvailability({
                token,
                emp_id,
                "day": "Monday",
                "start_time": monStart,
                "end_time": monEnd
            });
        }
        if (tueStart && tueEnd) {
            err = await addAvailability({
                token,
                emp_id,
                "day": "Tuesday",
                "start_time": tueStart,
                "end_time": tueEnd
            });
        }
        if (wedStart && wedEnd) {
            err = await addAvailability({
                token,
                emp_id,
                "day": "Wednesday",
                "start_time": wedStart,
                "end_time": wedEnd
            });
        }
        if (thuStart && thuEnd) {
            err = await addAvailability({
                token,
                emp_id,
                "day": "Thursday",
                "start_time": thuStart,
                "end_time": thuEnd
            });
        }
        if (friStart && friEnd) {
            err = await addAvailability({
                token,
                emp_id,
                "day": "Friday",
                "start_time": friStart,
                "end_time": friEnd
            });
        }
        if (satStart && satEnd) {
            err = await addAvailability({
                token,
                emp_id,
                "day": "Saturday",
                "start_time": satStart,
                "end_time": satEnd
            });
        }
        if (sunStart && sunEnd) {
            err = await addAvailability({
                token,
                emp_id,
                "day": "Sunday",
                "start_time": sunStart,
                "end_time": sunEnd
            });
        }

        if (typeof err.error !== 'undefined') {
            alert(err.error)
        } else {
            navigate("/employees");
        }
    }

    return (
        <>
            <main>
                <div className="avail">
                    <form onSubmit={handleSubmit} className="avail">
                        <h3>{first_name} {last_name}</h3>
                        <label>
                            Monday
                        </label>
                        <input type="time" value={monStart} onChange={e => setMonStart(e.target.value)}></input>
                        <input type="time" value={monEnd} onChange={e => setMonEnd(e.target.value)}></input>
                        <label>
                            Tuesday
                        </label>
                        <input type="time" value={tueStart} onChange={e => setTueStart(e.target.value)}></input>
                        <input type="time" value={tueEnd} onChange={e => setTueEnd(e.target.value)}></input>
                        <label>
                            Wednesday
                        </label>
                        <input type="time" value={wedStart} onChange={e => setWedStart(e.target.value)}></input>
                        <input type="time" value={wedEnd} onChange={e => setWedEnd(e.target.value)}></input>
                        <label>
                            Thursday
                        </label>
                        <input type="time" value={thuStart} onChange={e => setThuStart(e.target.value)}></input>
                        <input type="time" value={thuEnd} onChange={e => setThuEnd(e.target.value)}></input>
                        <label>
                            Friday
                        </label>
                        <input type="time" value={friStart} onChange={e => setFriStart(e.target.value)}></input>
                        <input type="time" value={friEnd} onChange={e => setFriEnd(e.target.value)}></input>
                        <label>
                            Saturday
                        </label>
                        <input type="time" value={satStart} onChange={e => setSatStart(e.target.value)}></input>
                        <input type="time" value={satEnd} onChange={e => setSatEnd(e.target.value)}></input>
                        <label>
                            Sunday
                        </label>
                        <input type="time" value={sunStart} onChange={e => setSunStart(e.target.value)}></input>
                        <input type="time" value={sunEnd} onChange={e => setSunEnd(e.target.value)}></input>
                        <button type="submit" id="submit">Submit</button>
                    </form>
                </div>
            </main>
        </>
    )
}