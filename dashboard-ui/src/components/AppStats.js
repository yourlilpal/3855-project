import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://kafka-3855.eastus2.cloudapp.azure.com/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>User</th>
							<th>Password</th>
						</tr>
						<tr>
							<td># User: {stats['num_of_name']}</td>
							<td># Password: {stats['num_of_password']}</td>
						</tr>
						{/*<tr>*/}
						{/*	<td colspan="2">Max BP Systolic: {stats['max_bp_sys_reading']}</td>*/}
						{/*</tr>*/}
						{/*<tr>*/}
						{/*	<td colspan="2">Max BR Diastolic: {stats['max_bp_dia_reading']}</td>*/}
						{/*</tr>*/}
						{/*<tr>*/}
						{/*	<td colspan="2">Max HR: {stats['max_bp_sys_reading']}</td>*/}
						{/*</tr>*/}
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_updated']}</h3>

            </div>
        )
    }
}