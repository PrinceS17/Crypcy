//Method to update object property


export const updateObject = (oldObject, updatedProperties) =>{
    return {
        ...oldObject, 
        ...updatedProperties
    }
}