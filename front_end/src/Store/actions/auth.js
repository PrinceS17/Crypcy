import axios from 'axios'
import * as actionTypes from './actionTypes';

export const getAcur = (acur, resData) =>{
    return {
        type: actionTypes.All_CUR,
        acur: acur,
        resData: resData,
    }
}
export const onMount = () => {
    return dispatch => {
        axios.get('http://34.216.221.19:8000/maker/basic/filter')
        .then(res=>{
            let resData = res.data;
            let acur = {};
            if(resData){
                console.log('onMount');
                console.log(resData);
                resData.forEach((cur)=>{
                    acur[cur.crypto_currency_id] = {
                        logo: cur.logo,
                        name: cur.name,
                    }
                })
                localStorage.setItem('acur',JSON.stringify(acur));
                localStorage.setItem('CurrencyData', JSON.stringify(resData));
                dispatch(getAcur(acur,resData));
            }
        })
    }
}

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
    localStorage.removeItem('rcmd');
    localStorage.removeItem('fav');
    localStorage.removeItem('acur');
    localStorage.removeItem('UserProfile');
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

export const setRcmd = (rcmd) =>{
    return {
        type: actionTypes.GET_RCMD,
        rcmd: rcmd,
    }
}

export const getRcmd = (username) =>{

    return dispatch =>{
        axios.get(`http://34.216.221.19:8000/users/advice/?username=${username}&num=5`)
        .then(res=>{
            localStorage.setItem('rcmd', JSON.stringify(res.data)); 
            console.log("Got RCMD");
            console.log(res.data);
            dispatch(setRcmd(res.data));

        }).catch(err=>{
            dispatch(authFail(err))
        });
    }
   
}


export const setFav = (fav) =>{
    return {
        type: actionTypes.UP_FAV,
        fav: fav,
    }
}
export const getFav = (username) =>{

    return dispatch =>{
        axios.get(`http://34.216.221.19:8000/profile/${username}/`)
        .then(res=>{
            localStorage.setItem('fav', JSON.stringify(res.data.favorite)); 
            console.log("Got FAV");
            console.log(res.data.favorite);
            dispatch(setFav(res.data.favorite));

        }).catch(err=>{
            dispatch(authFail(err))
        });
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
            dispatch(getRcmd(username));
            dispatch(getFav(username));
            dispatch(getProfile(username));
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
            dispatch(getRcmd(username));
            dispatch(getFav(username));
            dispatch(getProfile(username));
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
        const rcmds = JSON.parse(localStorage.getItem('rcmd'));
        const acurr = JSON.parse(localStorage.getItem('acur'));
        const favv = JSON.parse(localStorage.getItem('fav'));
        const resData = JSON.parse(localStorage.getItem('CurrencyData'));
        const userProfile = JSON.parse(localStorage.getItem('UserProfile'));

        if (token === undefined) {
            dispatch(logout());
        } else {
            const expirationDate = new Date(localStorage.getItem('expirationDate'));
            if ( expirationDate <= new Date() ) {
                dispatch(logout());
            } else {
                dispatch(setRcmd(rcmds));
                dispatch(setFav(favv));

                dispatch(getAcur(acurr,resData));
                dispatch(authSuccess(token, loguser));
                dispatch(checkAuthTimeout( (expirationDate.getTime() - new Date().getTime()) / 1000) );
                dispatch(storeProfile(userProfile));
            }
        }
    }
}

export const storeProfile = (profile)=>{
    return {
        type: actionTypes.STORE_PROFILE,
        profile: profile,
    }
}
export const getProfile = (username)=>{
    return dispatch =>{
        axios.get(`http://34.216.221.19:8000/profile/${username}`)
        .then((res)=>{
          localStorage.setItem('UserProfile', JSON.stringify(res.data))
          dispatch(storeProfile(res.data));
        });
        
    }
}

export const updateProfile = (username, updates) =>{
    return dispatch =>{
        const url = `http://34.216.221.19:8000/profile/${username}/`;//
        axios.patch(url, updates)
        .then(res=>{
            dispatch(getRcmd(username));
            dispatch(getProfile(username));
            if(updates.hasOwnProperty('favorite')){
                localStorage.setItem('fav',JSON.stringify(updates['favorite']));
                dispatch(setFav(updates['favorite']));///URL?? favorite??
                dispatch(getFav(username));
            }
        }).catch(err=>{
            console.log(err);
            dispatch(authFail(err));
        })
    }
}




