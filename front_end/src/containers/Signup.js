import React from 'react';
import { Form, Input, Icon, Button, Radio, Alert } from 'antd';
import { connect } from 'react-redux';
import { NavLink, withRouter } from 'react-router-dom';
import * as actions from '../store/actions/auth';
import ErrorCard from '../utilities/ErrorCard'

const FormItem = Form.Item;

class RegistrationForm extends React.Component {
  state = {
    confirmDirty: false,
  };
  componentDidMount(){
    this.props.clearError();
}
  handleSubmit = (e) => {
    e.preventDefault();
    this.props.form.validateFieldsAndScroll((err, values) => {
      if (!err) {
        this.props.onAuth(
            values.userName,
            values.gender,
            values.email,
            values.password,
            values.confirm,
            values.gender,
            values.interest,

        );
        // this.props.history.push('/');
      }
    });
  }

  handleConfirmBlur = (e) => {
    const value = e.target.value;
    this.setState({ confirmDirty: this.state.confirmDirty || !!value });
  }

  compareToFirstPassword = (rule, value, callback) => {
    const form = this.props.form;
    if (value && value !== form.getFieldValue('password')) {
      callback('Two passwords that you enter is inconsistent!');
    } else {
      callback();
    }
  }

  validateToNextPassword = (rule, value, callback) => {
    const form = this.props.form;
    if (value && this.state.confirmDirty) {
      form.validateFields(['confirm'], { force: true });
    }
    callback();
  }

  
  render() {
    let errorMessage = null;
    let errorBlock = null;

    if (this.props.error) {
        let errorData = this.props.error.response.data;
        console.log(errorData);
        errorMessage = (
            // <p>{this.props.error.message}</p>
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
                <Alert key='1' message={<div>{`Signup Successful! ${this.props.loguser}`} <br /><a href="/list/">Back to Homepage</a></div>} type="success" showIcon />
                :
                <div>
                     {errorMessage}
                    <Form onSubmit={this.handleSubmit} style={{width: "480px"}}>
                    <h1 style={{borderBottom: '2px solid'}}>Sign Up</h1>
                    <FormItem>
                        {getFieldDecorator('userName', {
                            rules: [{ required: true, message: 'Please input your username!' }],
                        })(
                            <Input prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />} placeholder="Username" />
                        )}
                    </FormItem>
                    <Form.Item label="Gender">
                        {getFieldDecorator('gender')(
                            <Radio.Group>
                            <Radio value="Male">Male</Radio>
                            <Radio value="Female">Female</Radio>
                            </Radio.Group>
                        )}
                    </Form.Item>
                    <FormItem>
                    {getFieldDecorator('email', {
                        rules: [{
                        type: 'email', message: 'The input is not valid E-mail!',
                        }, {
                        required: true, message: 'Please input your E-mail!',
                        }],
                    })(
                        <Input prefix={<Icon type="mail" style={{ color: 'rgba(0,0,0,.25)' }} />} placeholder="Email" />
                    )}
                    </FormItem>

                    <FormItem>
                    {getFieldDecorator('password', {
                        rules: [{
                        required: true, message: 'Please input your password!',
                        }, {
                        validator: this.validateToNextPassword,
                        }],
                    })(
                        <Input prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />} type="password" placeholder="Password" />
                    )}
                    </FormItem>

                    <FormItem>
                    {getFieldDecorator('confirm', {
                        rules: [{
                        required: true, message: 'Please confirm your password!',
                        }, {
                        validator: this.compareToFirstPassword,
                        }],
                    })(
                        <Input prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />} type="password" placeholder="Confirm Password" onBlur={this.handleConfirmBlur} />
                    )}
                    </FormItem>

                    <Form.Item label="Invest Interest (Risk Preference)">
                    {getFieldDecorator('interest')(
                        <Radio.Group>
                            <Radio.Button value="Low">Low</Radio.Button>
                            <Radio.Button value="Moderate">Moderate</Radio.Button>
                            <Radio.Button value="High">High</Radio.Button>
                        </Radio.Group>
                    )}
                    </Form.Item>

                    <FormItem>
                    <Button type="primary" htmlType="submit" style={{marginRight: '10px'}}>
                        Signup
                    </Button>


                    Or 
                    <NavLink 
                        style={{marginRight: '10px'}} 
                        to='/login/'> login
                    </NavLink>
                    </FormItem>

                </Form>

                </div>
            }
           

        </div>
    </div>
    );
  }
}

const WrappedRegistrationForm = Form.create()(RegistrationForm);

const mapStateToProps = (state) => {
    return {
        loading: state.loading,
        error: state.error,
        loguser: state.loguser
    }
}

const mapDispatchToProps = dispatch => {
    return {
        onAuth: (username, gender, email, password1, password2, interest) => dispatch(actions.authSignup(username, gender, email, password1, password2, interest)),
        clearError: ()=>dispatch(actions.clearError())

    }
}

export default connect(mapStateToProps, mapDispatchToProps)(WrappedRegistrationForm);
