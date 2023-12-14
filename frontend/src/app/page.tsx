"use client";

import React, { useState } from "react";
import axios from "axios";
export default function Home() {
    const [product, setProduct] = useState({
        merchant: "FKRT",
        url: "",
        name: "",
    });
    const [successful, setSuccessful] = useState(false);
    const handleChange = (e: any) => {
        setProduct({
            ...product,
            [e.target.name]: e.target.value,
        });
    };

    const submitProduct = async (e: any) => {
        e.preventDefault();
        console.log(product);
        const response = await axios.post("/api/link", product);
        if (response.status == 200) setSuccessful(true);
    };

    return (
        <main className='flex min-h-screen flex-col items-center  p-24'>
            <label className='text-white' htmlFor='merchant'>
                Merchant
                <select
                    id='merchant'
                    className='block p-3 bg-white border text-black border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500'
                    name='merchant'
                    value={product.merchant}
                    onChange={handleChange}
                >
                    <option value='FKRT'>Flipkart</option>
                    <option value='AMZN'>Amazon</option>
                </select>
            </label>
            <label className='text-white p-5' htmlFor='url'>
                URL
                <input
                    type='text'
                    className='block rounded-lg p-3 text-black'
                    placeholder='amazon/flipkart url'
                    name='url'
                    value={product.url}
                    onChange={handleChange}
                />
            </label>
            <label className='text-white p-5' htmlFor='url'>
                Name
                <input
                    type='text'
                    className='block rounded-lg p-3 text-black'
                    placeholder='Name of the product'
                    name='name'
                    value={product.name}
                    onChange={handleChange}
                />
            </label>
            {successful && (
                <h1 className='text-green-500'>Succesfully added</h1>
            )}
            <button
                className='bg-orange-500 p-5 py-2 rounded-full'
                onClick={submitProduct}
            >
                Track
            </button>
        </main>
    );
}
