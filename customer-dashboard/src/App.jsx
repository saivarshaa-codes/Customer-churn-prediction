import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import { useEffect } from 'react'
import axios from 'axios'
import { BASE_URL } from './api.js'
import CustomerSearch from './pages/CustomerSearch.jsx'
import ChurnPrediction from './pages/ChurnPrediction.jsx'
import ChurnSummary from './pages/ChurnSummary.jsx'
import HighRiskCustomers from './pages/HighRiskCustomers.jsx'

import './App.css'

function App() {
  // const[loading,setLoading] = useState(true);
  // const[data,setData] = useState(null);
  // const[error , setError] = useState(null);
  // useEffect( () => {
  //   axios.get(BASE_URL+"/churn/summary").then(
  //     (response) =>{
  //       setData(response.data);
  //       setLoading(false);
  //     }
  //   ).catch((error) =>{
  //     setError(error)
  //     setLoading(false)
  //   })
  // },[])

  return (
    <>
    {/* {loading?<h3>Loading...</h3>:error?<h3>Error occurred</h3>:<><h3>Data received</h3><p>Total Customers:{data.Total_Customers}</p><p>Total Churned:{data.Total_Churned}</p><p>Churn rate:{data.Churn_rate}</p></>} */}
    <ChurnSummary/>
    <h1>Customer Search</h1>
    <CustomerSearch/>
    
    <h1>Churn Prediction</h1>
    <ChurnPrediction/>
    </>
    
  )
}

export default App
