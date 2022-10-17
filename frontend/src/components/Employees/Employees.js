import React, { useState, useEffect } from 'react';
import { Routes, Route, Link, useNavigate } from "react-router-dom";
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

export default function Employees({ token }) {
    return (
        <div>
            <nav>
                <Link to="/employees">Employees</Link>
                <Link to="/employees/employee">Add Employee</Link>
            </nav>
            <Routes className="wrapper">
                <Route path="/" element={<ListEmployees token={token} />} />
                <Route path="/employee" element={<EmployeeDetails token={token} />} />
            </Routes>
        </div>
    )
}

function ListEmployees({ token }) {
    const [employees, setEmployees] = useState();

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

    }, [token])

    return (
        <>
            <main>
                <h2>Employees</h2>
                {employees && employees.map(data => (
                    <div key={data.id} className="employee">
                        <div className="name">{data.first_name} {data.last_name}</div>
                        DOB: <b>{data.DOB}</b> PTO: <b>{data.PTO_Days_Rem}</b>
                    </div>
                ))}
            </main>
        </>
    )
}

function EmployeeDetails({ token }) {
    const [first_name, setFirstName] = useState();
    const [last_name, setLastName] = useState();
    let navigate = useNavigate();

    const handleSubmit = async e => {
        e.preventDefault();

        const err = await addEmployee({
            first_name,
            last_name,
            token
        });

        if (typeof err.error !== 'undefined') {
            alert(err.error)
        } else {
            alert("Success! Employee has been added.");
            navigate("/employees");
        }
    }

    return (
        <>
            <main>
                <form onSubmit={handleSubmit}>
                    <h3>Add Employee</h3>
                    <label>
                        First name
                    </label>
                    <input type="text" placeholder="First Name" onChange={e => setFirstName(e.target.value)} />
                    <label>
                        First name
                    </label>
                    <input type="text" placeholder="Last Name" onChange={e => setLastName(e.target.value)} />
                    <button type="submit" id="submit">Submit</button>
                </form>
            </main>
        </>
    )
}
