import { Card, Alert } from 'antd';
import React from 'react';
import style from './ErrorCard.css'
class ErrorCard extends React.Component{
    
    
    render(){
        let errorData = this.props.data;
        let errorFields = Object.keys(errorData);
        console.log(errorData);
        let errorArray="";
        try{
            errorArray = errorFields.map((ef, idx)=>{
                let thisErr = errorData[ef].map((val, idx)=>{
                    return <p key={idx}>{val}</p>
                });
                let tt = `Error ${idx+1}: ${ef}`;
                return (
                    <Alert
                        message={tt}
                        className="ecCard"
                        key = {idx+1}
                        description={thisErr}
                        type="error"
                        showIcon
                        />
                )
            })
        }
        catch(error){
            console.log(error);
        }

        return (
            <div className="ecContainer">
            {errorArray}
            </div>
        )
    }
}


export default ErrorCard
