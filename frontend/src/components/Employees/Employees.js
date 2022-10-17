import React, { useState, useEffect } from 'react';
import { Routes, Route, Link } from "react-router-dom";
import './Employees.css'

export default function Employees({ token }) {
    return (
        <div>
            <nav>
                <Link to="/employees">Employees</Link>
                <Link to="/employees/employee">Employee</Link>
            </nav>
            <Routes className="wrapper">
                <Route path="/" element={<ListEmployees token={token} />} />
                <Route path="/employee" element={<EmployeeDetails />} />
            </Routes>
        </div>
    )
}

function ListEmployees({ token }) {
    const [employees, setEmployees] = useState()

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
                <h2>Many Employees</h2>
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

function EmployeeDetails() {
    return (
        <>
            <main>
                <h2>One Employee</h2>
            </main>
        </>
    )
}
