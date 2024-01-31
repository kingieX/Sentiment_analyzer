import {BrowserRouter, Routes, Route} from "react-router-dom";
import Register from "./Components/Register";
import Login from "./Components/Login";
import SentimentAnalyzer from "./SentimentAnalyzer";
import Home from "./Home";
import HelpAndSupport from "./HelpAndSupport";
import AboutPage from "./About";
import { AuthProvider } from "./AuthContext";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
          <Routes>
            <Route exact path="/" element={<SentimentAnalyzer />} />
            <Route exact path="/register" element={<Register />} />
            <Route exact path="/login" element={<Login />} />
            <Route exact  path="/home" element={<Home />} />
            <Route exact path="/help" element={<HelpAndSupport />} />
            <Route exact path="/about" element={<AboutPage />} />
          </Routes>
      </BrowserRouter>
    </AuthProvider>
    )
}

export default App;