import React, { useState, useEffect } from 'react';
import { Routes, Route, Link, useNavigate, useLocation } from "react-router-dom";
import './Holidays.css'

async function deleteHoliday(credentials) {
    return fetch('/api/deleteHoliday', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(res => res.json())
}

async function setHoliday(credentials) {
    return fetch('/api/setHoliday', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(res => res.json())
}

async function addHoliday(credentials) {
    return fetch('/api/addHoliday', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(res => res.json())
}

export default function Holidays({ token }) {
    return (
        <div className="hol-wrapper">
            <Routes>
                <Route path="/" element={<ListHolidays token={token} />} />
                <Route path="/holiday" element={<HolidayDetails token={token} />} />
            </Routes>
        </div>
    )
}

function ListHolidays({ token }) {
    const [employees, setHolidays] = useState();
    const [search, setSearch] = useState();
    const [refresh, setRefresh] = useState();

    useEffect(() => {
        fetch("/api/getHolidays", {
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
                setHolidays(data["holidays"]);
                console.log(data);
            }
        )

        setSearch("");

    }, [token, refresh])

    async function handleClick(hol_id) {
        let err = await deleteHoliday({
            token,
            hol_id
        })

        if (typeof err.error !== 'undefined') {
            alert(err.error);
        } else {
            setRefresh(hol_id);
        }
    }

    return (
        <>
            <main>
                <h2>Holidays</h2>
                <input type="text" placeholder="Search" className="search" onChange={e => setSearch(e.target.value)}></input>
                {employees && employees.filter(holiday => holiday.name.includes(search)).map(data => (
                    <div key={data.id} className="holiday">
                        <div className="name">{data.name}</div>
                        <div className="start">Start: <b>{data.start.split(" ")[0]}</b></div>
                        <div className="end">End: <b>{data.end.split(" ")[0]}</b></div>
                        <div className="left">
                            <Link to="/holidays/holiday" className="addemployee" state={{ data }}>Edit</Link>
                            <button className="addemployee" onClick={() => { handleClick(data.id) }}>Delete</button>
                        </div>
                    </div>
                ))}
                <Link to="/holidays/holiday" className="addButton">+</Link>
            </main>
        </>
    )
}

function HolidayDetails({ token }) {
    const [name, setName] = useState();
    const [hol_id, setHolId] = useState();
    const [start, setStart] = useState();
    const [end, setEnd] = useState();
    let navigate = useNavigate();
    let location = useLocation();

    useEffect(() => {
        if (location.state) {
            let data = location.state.data;
            console.log(data);
            setName(data.name);
            setHolId(data.id);
            setStart(data.start.split(" ")[0]);
            setEnd(data.end.split(" ")[0]);
        }
    }, [location.state])

    const handleSubmit = async e => {
        e.preventDefault();
        let err;

        if (hol_id) {
            err = await setHoliday({
                name,
                start,
                end,
                hol_id,
                token
            });
        } else {
            err = await addHoliday({
                name,
                start,
                end,
                token
            });
        }

        if (typeof err.error !== 'undefined') {
            alert(err.error)
        } else {
            navigate("/holidays");
        }
    }

    return (
        <>
            <main>
                <form onSubmit={handleSubmit}>
                    <h3>Holiday</h3>
                    <label>
                        Name
                    </label>
                    <input type="text" placeholder="Name" value={name} onChange={e => setName(e.target.value)} />
                    <label>
                        Start
                    </label>
                    <input type="date" value={start} onChange={e => setStart(e.target.value)} />
                    <label>
                        End
                    </label>
                    <input type="date" value={end} onChange={e => setEnd(e.target.value)} />
                    <button type="submit" id="submit">Submit</button>
                </form>
            </main>
        </>
    )
}