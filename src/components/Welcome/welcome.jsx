import React, { Component } from 'react'
import { Button } from 'semantic-ui-react'
import { Link } from 'react-router-dom'
import styles from './welcome.css'
import Logo from '../../Assets/Images/CrypcyLogo.png'
class Welcome extends Component{
    componentDidMount(){
        document.title = "Welcome to Crypcy";
    }
    render(){
        return (
            <div className = "Home">

                {/* <img className='Home-logo' src = {Logo} /> */}
                <h1 className="Home-header">Welcome to Crypcy</h1>
                <Link to="/list">
                <Button style={{position: "relative", top: "40px"}}>
                    Get Started
                </Button>  
                </Link> 

            </div>
        )
    }
}

export default Welcome;