import { useEffect,useState } from "react";
import axios from "axios";
import { BASE_URL } from "../api";


function ChurnPrediction(){
    const[tenure,setTenure]=useState("");
    const[monthlyCharges,setMonthlyCharges]=useState("");
    const[contractType,setContractType]=useState("Month-to-month");
    const[serviceCount,setServiceCount]=useState("");
    const[result,setResult] =useState(null)
    const[loading,setLoading]=useState(false);
    const[error,setError]=useState(null);

function handleSubmit(event){
    event.preventDefault();
    setLoading(true);
    setError(null)
    const body = {
        tenure:Number(tenure),
        monthly_charges:Number(monthlyCharges),
        contract_type:contractType,
        service_count: Number(serviceCount)

    }
    axios.post(BASE_URL+"/predict-churn",body).then(
        (response)=>{
            setResult(response.data);
            setLoading(false);
        }
    ).catch((error)=>{
        console.log(error.response)
        setLoading(false);
        setError(error.response?.status===422?error.response.data.detail[0].msg:"Something went wrong")
    });

}

    return(
        <>
        
        <form onSubmit={handleSubmit}>
            <label>Tenure</label>
            <input type="number" value={tenure} onChange={(event)=>{
                setTenure(event.target.value)
            }}/>
            <label>Monthly Charges</label>
            <input type="number" step="0.01" value={monthlyCharges} onChange={(event)=>{
                setMonthlyCharges(event.target.value)
            }}/>
            <label>Contract Type</label>
            <select value={contractType} onChange={(event)=>{
                setContractType(event.target.value)
            }}>
                <option value="">Select Contract Type</option>
                <option value="Month-to-month">Month-to-month</option>
                <option value ="One year">One year</option>
                <option value="Two year">Two year</option>
            </select>
            <label>Service Count</label>
            <input type="number" min="0" max="6" value={serviceCount} onChange={(event)=>{
                setServiceCount(event.target.value)
            }}/>
        <button type="submit">{loading?"Predicting...":"Predict"}</button>
        </form>
        {error && <p>{error}</p>}
        {result && (
        <>
        <p style={{backgroundColor:result.risk_score<0.3?"green":result.risk_score<=0.6?"orange":"red"}}>
            Risk Score:{(result.risk_score*100).toFixed(1)}%</p>
        <p>Prediction:{result.prediction}</p>
        </>

)}
        </>

    )

}
export default ChurnPrediction

