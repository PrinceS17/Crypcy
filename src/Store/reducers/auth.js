import * as actionTypes from '../actions/actionTypes';
import { updateObject } from '../utility';

const initialState = {
    token: null,
    error: null, 
    loading: false,
    loguser: null,
    rcmd: null,
    fav: null,
    allCurrency: null,
    CurrencyList: null,
}
const upAllCur = (state, action) => {
    console.log(action);
    console.log("resData");
    return updateObject(state, {
        allCurrency: action.acur,
        CurrencyList: action.resData,
    });
}



const authStart = (state, action) => {
    return updateObject(state, {
        error: null,
        loading: true
    });
}

const authSuccess = (state, action) => {
    return updateObject(state, {
        token: action.token,
        error: null,
        loading: false,
        loguser: action.loguser
    });
}

const authFail = (state, action) => {
    return updateObject(state, {
        error: action.error,
        loading: false
    });
}

const authLogout = (state, action) => {
    return updateObject(state, {
        token: null,
        loguser: null,
        fav: null,
        rcmd: null,
        fav: null,
        allCurrency: null,
        CurrencyList: null,
    });
}

const authClearError = (state, action)=>{
    return updateObject(state, {
        error: null,
    });   
}

const getRcmd = (state, action)=>{
    return updateObject(state, {
        rcmd: action.rcmd,
    });   
}
const upFav = (state, action) =>{
    return updateObject(state, {
        fav: action.fav,
    });   
}

const storeProfile = (state, action) =>{
    return updateObject(state, {
        Profile: action.profile
    })
}
const reducer = (state=initialState, action) => {
    switch (action.type) {
        case actionTypes.AUTH_START: return authStart(state, action);
        case actionTypes.AUTH_SUCCESS: return authSuccess(state, action);
        case actionTypes.AUTH_FAIL: return authFail(state, action);
        case actionTypes.AUTH_LOGOUT: return authLogout(state, action);
        case actionTypes.AUTH_CLEARERROR: return authClearError(state, action);
        case actionTypes.GET_RCMD: return getRcmd(state, action);
        case actionTypes.UP_FAV: return upFav(state, action);
        case actionTypes.All_CUR: return upAllCur(state, action);
        case actionTypes.STORE_PROFILE: return storeProfile(state,action);
        default:
            return state;
    }
}

export default reducer;