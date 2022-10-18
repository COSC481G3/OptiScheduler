import React, { useState, useEffect } from 'react';
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

export default function Store({ token }){
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
                setStoreName(data.name);
                setStoreAddress(data.address);
                console.log(data);
            }
        )
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
            <main className="store-wrapper">
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
                </form>
            </main>
        </>
    )
}