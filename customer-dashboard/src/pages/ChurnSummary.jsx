import { useEffect, useState } from "react";
import { BASE_URL } from "../api";
import axios from "axios";

function ChurnSummary(){
    const[data,setData]=useState(null)
    const [loading,setLoading]=useState(true)
    const [error,setError]=useState(null)
    useEffect(()=>{
        
        axios.get(BASE_URL+"/churn/summary").then(
            (response)=>{
                
                setData(response.data)
                setLoading(false)
            }
        ).catch((error)=>{
            
            setError("Something went wrong")
            setLoading(false)
        })

    },[]);
    return(
            <>
            {loading && <div className="spinner"></div>}
            {error && <p>{error}</p>}
            { data && (
            <>
            <h1>Churn Analysis</h1>
            <p>Shows the customer churn details </p>
            <p>Total Customers: {data.Total_Customers}</p>
            <p>Total Churned : {data.Total_Churned}</p>
            <p>Churn rate: {(data.Churn_rate *100).toFixed(1)}%</p>
            <table>
                <thead>
                    <tr>
                        <th>Contract Type</th>
                        <th>Churn Rate</th>
                        <th>Visual</th>
                    </tr>
                </thead>
                
                <tbody>
                    {data.Churn_rate_by_contract_Type.map((contract)=>(
                        <tr key={contract.contract_type}>
                            <td>{contract.contract_type}</td>
                            <td>{contract.churn_rate.toFixed(1)}%</td>
                            <td>
                                <div className="bar"
                                style={{width:contract.churn_rate +"%"}}></div>
                            </td>
                        </tr> 
                    ))}
                </tbody>
                
            </table>
            </>
        )}
        </>
)
}

export default ChurnSummary;