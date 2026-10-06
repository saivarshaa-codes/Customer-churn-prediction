import { useEffect, useState } from "react";
import { BASE_URL } from "../api";
import axios from "axios";

function HighRiskCustomers(){
    const[limit,setLimit]=useState(50);
    const[data,setData]=useState(null);
    const[loading,setLoading]=useState(true);
    const[error,setError]=useState(null);
    const[sortAsc,setSortAsc]=useState(true);
    useEffect(()=>{
        
        axios.get(BASE_URL+"/customers/high-risk?limit="+limit).then(
            (response)=>{
                setData(response.data);
                setLoading(false);
            }
        ).catch(()=>{
            setError("Something went wrong")
            setLoading(false)
        })
        
    },[limit])
    

    return(
        <>
        {loading && <div className="spinner"></div>}
        {error && <p>{error}</p>}
        {data && (
            <>
            {data.length===0?<p>No high risk customers found</p>:
            <>
            <p>{data.length} high risk customers identified</p>
            <table>
            <thead>
                <tr>
                    <th>Customer ID</th>
                    <th onClick={()=>{
                        setSortAsc(!sortAsc);
                    }}>Tenure</th>
                    <th>Monthly Charges</th>
                    <th>Contract Type</th>
                    <th>Risk Reason</th>
                </tr>
            </thead>
            <tbody>
                {[...data].sort((a,b)=>
                sortAsc?a.tenure-b.tenure:b.tenure-a.tenure
                ).map((customer)=>(
                    <tr key = {customer.customer_id}>
                        <td>{customer.customer_id}</td>
                        <td>{customer.tenure}</td>
                        <td>{"$"+customer.monthly_charges.toFixed(2)}</td>
                        <td>{customer.contract_type}</td>
                        <td>{customer.risk_reason}</td>
                    </tr>

                ))}
            </tbody>
        </table>
            </>
            } 
            </>
        )}
        {data && data.length>0 &&
        <button onClick={()=>{
            setLimit(limit+50);
        }}>Load More</button>
    }
        </>
    )

}
export default HighRiskCustomers;