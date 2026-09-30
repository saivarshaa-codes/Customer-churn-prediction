import axios from "axios";
import { useState } from "react";
import { BASE_URL } from "../api";
function CustomerSearch(){
const [customerID,setCustomerID] = useState("");
const[data,setData]=useState(null)
const [loading,setLoading]=useState(false)
const[error,setError]=useState(null)
return(
    <>
    {loading && <div className="spinner"></div>}
    <input className="customer-search" value={customerID} onChange={(event)=>{
        setCustomerID(event.target.value)
    }}/>
    <button className="search-button" onClick={()=>{
        setLoading(true)
        
        axios.get(BASE_URL+"/customer/"+customerID).then(
            (response)=>{
                setLoading(false)
                setData(response.data)
            }
        ).catch(
            (error)=>{
                setLoading(false)
                error.response?.status===404?setError("Customer Not Found"):setError("Something went wrong")
            }
        )

    }}>Search</button>
    {error && <p>{error}</p>}
    {data && (
        <div className="card">
            <p>Customer ID:{data.customer_id}</p>
            <p>Tenure : {data.tenure}</p>
            <p>Contract Type:{data.contract_type}</p>
            <p>Monthly charges :{data.monthly_charges}</p>
            <p style ={{backgroundColor : data.churn===1?"red":"green"}}>Churn: {data.churn==1?"Churn":"Active"}</p>
        </div>
    )}
    </>
    )

}

export default CustomerSearch