import axios from 'axios'
import * as actionTypes from './actionTypes';

export const authStart = () => {
    return {
        type: actionTypes.AUTH_START
    }
}

export const authSuccess = (token, loguser) => {
    return {
        type: actionTypes.AUTH_SUCCESS,
        token: token,
        loguser: loguser,
    }
}

export const authFail = error => {
    return {
        type: actionTypes.AUTH_FAIL,
        error: error
    }
}

export const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('expirationDate');
    localStorage.removeItem('loguser');
    return {
        type: actionTypes.AUTH_LOGOUT,
        loguser: null
    };
}

export const clearError = () =>{
    return {
        type: actionTypes.AUTH_CLEARERROR,
    }
}

export const checkAuthTimeout = expirationTime => {
    return dispatch => {
        setTimeout(() => {
            dispatch(logout());
        }, expirationTime * 1000)
    }
}


export const authLogin = (username, password) => {
    return dispatch => {
        dispatch(authStart());

          axios.post('http://34.216.221.19:8000/rest-auth/login/', {
            username: username,
            password: password,
            
        })
        .then(res => {
            const token = res.data.key;
            console.log(res.headers);
            const expirationDate = new Date(new Date().getTime() + 3600 * 1000);
            localStorage.setItem('token', token);
            localStorage.setItem('loguser', username);
            localStorage.setItem('expirationDate', expirationDate);
            dispatch(authSuccess(token, username));
            dispatch(checkAuthTimeout(3600));
        })
        .catch(err => {
            dispatch(authFail(err))
        })
    }
}

export const authSignup = (username, gender, email, password1, password2, interest) => {
    return dispatch => {
        dispatch(authStart());
        axios.post('http://34.216.221.19:8000/rest-auth/registration/', {
            username: username,
            email: email,
            password1: password1,
            password2: password2,
            gender: gender,
            interest_tag: interest
        })
        .then(res => {
            const token = res.data.key;
            const expirationDate = new Date(new Date().getTime() + 3600 * 1000);
            localStorage.setItem('token', token);
            localStorage.setItem('loguser', username);
            localStorage.setItem('expirationDate', expirationDate);
            dispatch(authSuccess(token,username));
            dispatch(checkAuthTimeout(3600));
        })
        .catch(err => {
            dispatch(authFail(err))
        })
    }
}

export const authCheckState = () => {
    return dispatch => {
        const token = localStorage.getItem('token');
        const loguser = localStorage.getItem('loguser');
        if (token === undefined) {
            dispatch(logout());
        } else {
            const expirationDate = new Date(localStorage.getItem('expirationDate'));
            if ( expirationDate <= new Date() ) {
                dispatch(logout());
            } else {
                dispatch(authSuccess(token, loguser));
                dispatch(checkAuthTimeout( (expirationDate.getTime() - new Date().getTime()) / 1000) );
            }
        }
    }
}
