import React, { useState, useEffect } from 'react';
import { Routes, Route, Link, useNavigate, useLocation } from "react-router-dom";
import './Store.css'

async function setStore(credentials) {
    return fetch('/api/setStore', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(res => res.json())
}

async function addHours(credentials) {
    return fetch('/api/addHours', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(res => res.json())
}

async function deleteHours(credentials) {
    return fetch('/api/deleteHours', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(res => res.json())
}

export default function Store({ token }) {
    return (
        <div className="store-wrapper">
            <Routes>
                <Route path="/" element={<StoreDetails token={token} />} />
                <Route path="/hours" element={<StoreHours token={token} />} />
            </Routes>
        </div>
    )
}

function StoreDetails({ token }){
    const [store_name, setStoreName] = useState();
    const [store_address, setStoreAddress] = useState();

    useEffect(() => {
        fetch("/api/getStore", {
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
                if(data.name === " "){
                    setStoreName("");
                } else {
                    setStoreName(data.name);
                }

                if(data.address === " "){
                    setStoreAddress("");
                } else {
                    setStoreAddress(data.address);
                }

                console.log(data);
            }
        );
    }, [token])

    const handleSubmit = async e => {
        e.preventDefault();
        let err;

        err = await setStore({
            store_name,
            store_address,
            token
        })

        if (typeof err.error !== 'undefined') {
            alert(err.error);
        } else {
            alert(err.success);
        }
    }

    return (
        <>
            <main id="store">
                <form onSubmit={handleSubmit}>
                    <h3>Store</h3>
                    <label>
                        Name
                    </label>
                    <input type="text" placeholder="Store Name" value={store_name} onChange={e => setStoreName(e.target.value)} />
                    <label>
                        Address
                    </label>
                    <input type="text" placeholder="Store Address" value={store_address} onChange={e => setStoreAddress(e.target.value)} />
                    <button type="submit" id="submit">Submit</button>
                    <Link className="altbutton" to="/store/hours" state={{ store_name }}>Edit Hours</Link>
                </form>
            </main>
        </>
    )
}

function StoreHours({ token }) {
    const [store_name, setStoreName] = useState();

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
            let store_name = location.state.store_name;
            console.log("Hours");
            setStoreName(store_name);
            console.log(store_name);

            fetch("/api/getHours", {
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
                    let hours = data["hours"];
                    console.log(hours);
                    hours.forEach((day) => {
                        if(day.open_time.length === 7){
                            day.open_time = "0" + day.open_time;
                        }
                        if(day.close_time.length === 7){
                            day.close_time = "0" + day.close_time;
                        }

                        if(day.day === "Monday"){
                            setMonStart(day.open_time);
                            setMonEnd(day.close_time);
                        } else if(day.day === "Tuesday"){
                            setTueStart(day.open_time);
                            setTueEnd(day.close_time);
                        } else if(day.day === "Wednesday"){
                            setWedStart(day.open_time);
                            setWedEnd(day.close_time);
                        } else if(day.day === "Thursday"){
                            setThuStart(day.open_time);
                            setThuEnd(day.close_time);
                        } else if(day.day === "Friday"){
                            setFriStart(day.open_time);
                            setFriEnd(day.close_time);
                        } else if(day.day === "Saturday"){
                            setSatStart(day.open_time);
                            setSatEnd(day.close_time);
                        } else if(day.day === "Sunday"){
                            setSunStart(day.open_time);
                            setSunEnd(day.close_time);
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
            err = await addHours({
                token,
                "day": "Monday",
                "open_time": monStart,
                "close_time": monEnd
            });
        }
        if (tueStart && tueEnd) {
            console.log(tueEnd);
            err = await addHours({
                token,
                "day": "Tuesday",
                "open_time": tueStart,
                "close_time": tueEnd
            });
        }
        if (wedStart && wedEnd) {
            err = await addHours({
                token,
                "day": "Wednesday",
                "open_time": wedStart,
                "close_time": wedEnd
            });
        }
        if (thuStart && thuEnd) {
            err = await addHours({
                token,
                "day": "Thursday",
                "open_time": thuStart,
                "close_time": thuEnd
            });
        }
        if (friStart && friEnd) {
            err = await addHours({
                token,
                "day": "Friday",
                "open_time": friStart,
                "close_time": friEnd
            });
        }
        if (satStart && satEnd) {
            err = await addHours({
                token,
                "day": "Saturday",
                "open_time": satStart,
                "close_time": satEnd
            });
        }
        if (sunStart && sunEnd) {
            err = await addHours({
                token,
                "day": "Sunday",
                "open_time": sunStart,
                "close_time": sunEnd
            });
        }

        if (typeof err.error !== 'undefined') {
            alert(err.error)
        } else {
            navigate("/store");
        }
    }

    async function onDeleteHours(day){
        let err = await deleteHours({
            token,
            day
        });

        if (typeof err.error !== 'undefined') {
            alert(err.error);
        } else {
            if(day === "Monday"){
                setMonStart("");
                setMonEnd("");
            } else if(day === "Tuesday"){
                setTueStart("");
                setTueEnd("");
            } else if(day === "Wednesday"){
                setWedStart("");
                setWedEnd("");
            } else if(day === "Thursday"){
                setThuStart("");
                setThuEnd("");
            } else if(day === "Friday"){
                setFriStart("");
                setFriEnd("");
            } else if(day === "Saturday"){
                setSatStart("");
                setSatEnd("");
            } else if(day === "Sunday"){
                setSunStart("");
                setSunEnd("");
            }
        }
    }

    return (
        <>
            <main>
                <div className="hours">
                    <form onSubmit={handleSubmit} className="avail">
                        <h3>{store_name}</h3>
                        <label>
                            Monday
                        </label>
                        <input type="time" value={monStart} onChange={e => setMonStart(e.target.value)}></input>
                        <input type="time" value={monEnd} onChange={e => setMonEnd(e.target.value)}></input>
                        <button type="button" className="deleteHours" onClick={() => { onDeleteHours("Monday") }}>Delete</button>
                        <label>
                            Tuesday
                        </label>
                        <input type="time" value={tueStart} onChange={e => setTueStart(e.target.value)}></input>
                        <input type="time" value={tueEnd} onChange={e => setTueEnd(e.target.value)}></input>
                        <button type="button" className="deleteHours" onClick={() => { onDeleteHours("Tuesday") }}>Delete</button>
                        <label>
                            Wednesday
                        </label>
                        <input type="time" value={wedStart} onChange={e => setWedStart(e.target.value)}></input>
                        <input type="time" value={wedEnd} onChange={e => setWedEnd(e.target.value)}></input>
                        <button type="button" className="deleteHours" onClick={() => { onDeleteHours("Wednesday") }}>Delete</button>
                        <label>
                            Thursday
                        </label>
                        <input type="time" value={thuStart} onChange={e => setThuStart(e.target.value)}></input>
                        <input type="time" value={thuEnd} onChange={e => setThuEnd(e.target.value)}></input>
                        <button type="button" className="deleteHours" onClick={() => { onDeleteHours("Thursday") }}>Delete</button>
                        <label>
                            Friday
                        </label>
                        <input type="time" value={friStart} onChange={e => setFriStart(e.target.value)}></input>
                        <input type="time" value={friEnd} onChange={e => setFriEnd(e.target.value)}></input>
                        <button type="button" className="deleteHours" onClick={() => { onDeleteHours("Friday") }}>Delete</button>
                        <label>
                            Saturday
                        </label>
                        <input type="time" value={satStart} onChange={e => setSatStart(e.target.value)}></input>
                        <input type="time" value={satEnd} onChange={e => setSatEnd(e.target.value)}></input>
                        <button type="button" className="deleteHours" onClick={() => { onDeleteHours("Saturday") }}>Delete</button>
                        <label>
                            Sunday
                        </label>
                        <input type="time" value={sunStart} onChange={e => setSunStart(e.target.value)}></input>
                        <input type="time" value={sunEnd} onChange={e => setSunEnd(e.target.value)}></input>
                        <button type="button" className="deleteHours" onClick={() => { onDeleteHours("Sunday") }}>Delete</button>
                        <button type="submit" id="submit">Submit</button>
                    </form>
                </div>
            </main>
        </>
    )
}