import { createContext, useContext, useState } from "react";

export const AppContext = createContext(null)

const AppContextProvider = ({children}) => {
    const [accessToken, setAccessToken] = useState('');
    const [selectedURLID, setSelectedURLID] = useState('');

    return <AppContext.Provider value={{
        accessToken,
        setAccessToken,
        selectedURLID,
        setSelectedURLID
    }}>{children}</AppContext.Provider>
}

export const useAppContext = () => {
    return useContext(AppContext)
}

export default AppContextProvider