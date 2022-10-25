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
                console.log(data);
            }
        )

        setSearch("");

    }, [token, refresh])

    async function handleClick(emp_id){
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
            <main>
                <h2>Employees</h2>
                <input type="text" placeholder="Search" className="search" onChange={e => setSearch(e.target.value)}></input>
                {employees && employees.filter(employee => employee.first_name.includes(search) || employee.last_name.includes(search)).map(data => (
                    <div key={data.id} className="employee">
                        <div className="name">{data.first_name} {data.last_name}</div>
                        <div className="dob">DOB: <b>{data.DOB}</b></div>
                        <div className="pto">PTO: <b>{data.PTO_Days_Rem}</b></div>
                        <div className="left">
                            <Link to="/employees/employee" className="addemployee" state={{ data }}>Edit</Link>
                            <button className="addemployee" onClick={() => {handleClick(data.id)}}>Delete</button>
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
    let navigate = useNavigate();
    let location = useLocation();

    useEffect(() => {
        if(location.state){
            let data = location.state.data;
            console.log(data);
            setFirstName(data.first_name);
            setLastName(data.last_name);
            setEmpID(data.id);
        }
    }, [location.state])

    const handleSubmit = async e => {
        e.preventDefault();
        let err;

        if(emp_id){
            err = await setEmployee({
                first_name,
                last_name,
                token,
                emp_id
            })
        } else {
            err = await addEmployee({
                first_name,
                last_name,
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
                    <button type="submit" id="submit">Submit</button>
                </form>
            </main>
        </>
    )
}
