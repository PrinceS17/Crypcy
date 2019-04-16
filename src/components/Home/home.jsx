import React, { Component } from 'react'
import { Button } from 'semantic-ui-react'
import { Link } from 'react-router-dom'
import styles from './home.css'

class Home extends Component{
    render(){
        return (
            <div className = "Home">
                <img className='Home-logo' src = 'https://www.shareicon.net/data/128x128/2016/07/08/117420_bitcoin_512x512.png' />
                <h1 className="Home-header">Crypcy Demo</h1>
                <Link to="/list">
                <Button>
                    List View
                </Button>  
                </Link> 


                <Link to="/adv">
                <Button>
                    Advanced Functions
                </Button>  
                </Link> 



            </div>
        )
    }
}

export default Home;