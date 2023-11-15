import './App.css'
import Login from './components/Login'
import {
  Navigate,
  Route,
  Routes
} from 'react-router-dom'
import Signup from './components/Signup'
import Dashboard from './components/Dashboard'
import { useEffect } from 'react'
import { useAppContext } from './context/appContext'
import URLLogs from './components/URLLogs'

function App() {
  const {accessToken, setAccessToken} = useAppContext();
  const accessTokenFromStorage = localStorage.getItem('access_token') || accessToken ;

  useEffect(() => {
    if((!accessToken || accessToken === "") && accessTokenFromStorage) {
      setAccessToken(accessTokenFromStorage)
    }
  }, [])

  const logoutUser = () => {
      localStorage.clear();
      setAccessToken('');
      navigate(LOGIN_ROUTE)
  }


  return (
   <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/login"  element={accessTokenFromStorage ? <Navigate to="/dashboard" replace /> :  <Login />} />
      <Route path="/register" element={accessTokenFromStorage ? <Navigate to="/dashboard" replace /> :  <Signup />}  />
      <Route path="/dashboard" element={accessTokenFromStorage ?   <Dashboard /> : <Navigate to="/login" replace />} />
      <Route path="/urlLogs" element={accessTokenFromStorage ?   <URLLogs /> : <Navigate to="/login" replace />} />
   </Routes>
  )
}

export default App
