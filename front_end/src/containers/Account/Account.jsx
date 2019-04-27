import React, { Component } from 'react'
import axios from 'axios'
import {Alert} from 'antd'
import { Link, withRouter } from 'react-router-dom'
import {connect} from 'react-redux'


class Account extends Component{

    constructor(props){
        super(props);
        this.state={
            userProfile: [],
        }
        this.fetchUser = this.fetchUser.bind(this);
    }
    
    fetchUser(){
       
        
    }
    
    render(){

        if((typeof this.props.isAuthenticated == undefined)|| !this.props.isAuthenticated){
            let desc = (
                <a href='/login'> Log in again </a>
            );
            return (
                <Alert 
                    message="You have logged out"
                    description={desc}
                    type="error"
                    showIcon
                />
            );
        }


        else{
            
            axios.get('http://34.216.221.19:8000/rest-auth/user/')
            .then( (res) =>{
                console.log(res);
            }).catch(err=>{
                console.log(err);   
            });

            return (
                <div>
                    

                </div>
            )
        }   
    }
}


const mapStateToProps = (state) => {
    return {
        loguser: state.loguser,
        isAuthenticated: state.token !== null

    }
  }

  

  export default withRouter(connect(mapStateToProps, null)(Account));