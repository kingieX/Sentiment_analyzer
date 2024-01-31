
import { useNavigate, Link } from "react-router-dom";

const SentimentAnalyzer = () => {
  const navigate = useNavigate();

  const BackToHome = () => {
    navigate("/");
  }

  const HandleSignUp = () => {
    navigate("/register");
  }

  const HandleLogIn = () => {
    navigate("/login");
  }

  return (
    <div>
      {/* <div className="bg-black-700 flex pl-7 pr-7">
        <h1 className="text-green-600 mb-2 text-2xl mt-4 font-bold" onClick={BackToHome}>Sentiment Analyzer</h1>
      </div> */}
      {/*  */}
      <div className="body flex justify-around items-center">
        <div className="body left flex flex-col justify-center items-center gap-4 h-screen">
          <h1 className="text-green-600 mb-2 text-2xl mt-4 font-bold" onClick={BackToHome}>Sentiment Analyzer</h1>
          <div className="">
            <h1 className="text-3xl font-bold"><span className="text-red-500">Explore,</span> <span className="text-green-500">Understand</span> <span className="text-yellow-500">& Analyze</span></h1>
            <h2 className="text-3xl text-white">Nigerian social media text...</h2>
          </div>
        </div>
        <div className="body right flex text-white flex-col justify-between items-center">
          <div></div>
          <div>
            <h1 className="text-3xl font-bold mb-10">Let's get you started</h1>
            <button onClick={HandleLogIn} className="bg-green-500 px-6 py-2 rounded-md mr-6 hover:bg-green-400">Log in</button>
            <button onClick={HandleSignUp} className="bg-green-500 px-6 py-2 rounded-md ml-6 hover:bg-green-400">Sign up</button>
          </div>
          <div>
            <h1 className="text-gray-400 p-4"><span><Link to='/help'>Help & Support</Link></span> | <span><Link to='/about'>About</Link></span></h1>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SentimentAnalyzer;