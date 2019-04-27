import React from 'react';
import { Form, Icon, Input, Button, Spin, Alert } from 'antd';
import { connect } from 'react-redux';
import { Link, NavLink } from 'react-router-dom';
import * as actions from '../store/actions/auth';
import ErrorCard from '../utilities/ErrorCard'

const FormItem = Form.Item;
const antIcon = <Icon type="loading" style={{ fontSize: 24 }} spin />;


class NormalLoginForm extends React.Component {

componentDidMount(){
    this.props.clearError();
    document.title = "Login";
    window.scrollTo(0, 0);

}
  handleSubmit = (e) => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        this.props.onAuth(values.userName, values.password);
        this.props.history.push(this.props.location.pathname);
      }
    });
  }

  render() {
    let errorMessage = null;
    let errorBlock = null;

    if (this.props.error) {
        
        let errorData = this.props.error.response.data;
        console.log(errorData);
        errorMessage = (

        <div>
            <ErrorCard data = {errorData}/>
        </div>

        );
        
    }

    const { getFieldDecorator } = this.props.form;
    return (
        <div style={{position:'relative'}}>
        <div style={{position: 'absolute', left: '50%', width: '50%', transform: "translate(-50%, 0)"}}>

            {
                this.props.loguser?
                <Alert  key='1' message={<div>{`You are logged in! ${this.props.loguser}`} <br /><Link to="/list/">Back to List view</Link></div>} type="success"  showIcon/>
                :
                <div>
                    {errorMessage}
                
                    {
                        this.props.loading ?

                        <Spin indicator={antIcon} />

                        :

                        <Form onSubmit={this.handleSubmit} className="login-form">
                            <h1 style={{borderBottom: '2px solid'}}>Log In</h1>
                            <FormItem style={{width: '480px'}}>
                            {getFieldDecorator('userName', {
                                rules: [{ required: true, message: 'Please input your username!' }],
                            })(
                                <Input prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />} placeholder="Username" />
                            )}
                            </FormItem>

                            <FormItem style={{width: '480px'}}>
                            {getFieldDecorator('password', {
                                rules: [{ required: true, message: 'Please input your Password!' }],
                            })(
                                <Input prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />} type="password" placeholder="Password" />
                            )}
                            </FormItem>

                            <FormItem style={{width: '480px'}}>
                            <Button type="primary" htmlType="submit" style={{marginRight: '10px'}}>
                                Login
                            </Button>
                            Or 
                            <Link 
                                style={{marginRight: '10px'}} 
                                to='/signup/'> signup
                            </Link>
                            </FormItem>
                        </Form>
                    }

                </div>       

                
                }
           
            
            
      </div>
      </div>
    );
  }
}

const WrappedNormalLoginForm = Form.create()(NormalLoginForm);

const mapStateToProps = (state) => {
    return {
        loading: state.loading,
        error: state.error,
        loguser: state.loguser
    }
}

const mapDispatchToProps = dispatch => {
    return {
        onAuth: (username, password) => dispatch(actions.authLogin(username, password)),
        clearError: ()=>dispatch(actions.clearError())
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(WrappedNormalLoginForm);