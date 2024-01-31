import chatIcon from './assets/chatIcon.png';
import deleteIcon from './assets/deleteIcon.png';
import menuIcon from './assets/menuIcon.png';
import copyIcon from './assets/copyIcon.png';
import thumbUp from './assets/thumpUp.png';
import thumbDown from './assets/thumbDown.png';
import searchIcon from './assets/searchIcon.png';
import { useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import { useNavigate } from 'react-router-dom';


const Home = () => {
    const navigate = useNavigate();
    const [inputText, setInputText] = useState('');
    const [result, setResult] = useState(null);
    // get user Details
    const { logout, userId, accessToken } = useAuth();
    const [userDetails, setUserDetails] = useState(null);
   
    // fetch user details
    useEffect(() => {
        const fetchUserDetails = async () => {
          try {
            const response = await fetch(`http://127.0.0.1:8000/users/${userId}`, {
              headers: {
                Authorization: `Bearer ${accessToken}`,
              },
            });
    
            const data = await response.json();
            setUserDetails(data);
          } catch (error) {
            console.error('Error fetching user details:', error);
          }
        };
    
        if (userId) {
          fetchUserDetails();
        }
    }, [userId, accessToken]);

    // handle logout
    const handleLogout = () => {
        // Call the logout function from the authentication context
        logout();
    
        // Redirect to the home page
        navigate('/');
      };

    // post user input sentiment text
    const analyzeSentiment = async () => {
        try {
          const response = await fetch('https://xclasscode-sentiment-analyzer.hf.space/analyze_sentiment', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text_input: inputText }),
          });
        //   console.log(response);

          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
    
          const data = await response.json();
          setResult(data);
        } catch (error) {
          console.error('Error analyzing sentiment:', error);

           // If available, log the error details from the API response
            if (error.response) {
                try {
                const errorData = await error.response.json();
                console.error('API Error:', errorData);
                } catch (parseError) {
                console.error('Error parsing API response:', parseError);
                }
            }
        }
      };


    const handleInputChange = (event) => {
    
        // Dynamically adjust the height of the textarea
        event.target.style.height = 'auto';
        event.target.style.height = `${event.target.scrollHeight}px`;
        // setInputText(event.target.value)
      };

  return (
    <div className="body flex justify-between items-center h-full">
        {/* left side */}
        <div className='right flex flex-col justify-between w-1/4 h-screen'>
            <div>
                <h1 className='text-green-600 text-2xl m-2 font-bold'>Sentiment Analyzer</h1>
                <div className='border border-gray-700'></div>
                <div className='mx-4 text-white'>
                    <div>
                        <h1 className='text-gray-400 font-semibold text-xl mb-2'>History</h1>
                        {/* <h2 className='text-gray-400 text-md font-semibold'>{Today}</h2> */}

                        {result ? (
                            <div className='flex flex-row py-2 justify-between items-center px-2 bg-gray-600 mb-2 rounded'>
                            <img src={chatIcon} alt="chat" />
                            <p className='font-semibold'>{result.text_input.substring(0,21)}...</p>
                            <img src={deleteIcon} alt="deleteicon" />
                        </div>
                        ) : (
                            <p className='text-center'>No history...</p>
                        )}
                    </div>
                    {/* <div>
                        <h2 className='text-gray-400 text-md font-semibold'>{previous}</h2>
                        <div className='flex flex-row py-2 justify-between items-center px-4 bg-gray-60 mb-2 rounded'>
                            <img src={chatIcon} alt="chat" />
                            <p className='-ml-10 font-semibold'>{history}</p>
                            <img src={deleteIcon} alt="deleteicon" />
                        </div>
                    </div> */}
                </div>
            </div>
            {/* user details */}
            {userDetails ? (
                <div className='text-white'>
                <div className='border border-gray-700'></div>
                <div className='flex justify-between items-center my-4 mx-3'>
                    {/* <img src="" alt="profile img" className='w-8 h-8 bg-white' /> */}
                    <div className='w-10 h-10 bg-green-600 flex justify-center items-center rounded-full'>
                        <p className='text-white font-bold'>{userDetails.username.charAt(0).toUpperCase()}</p>
                    </div>
                    <div className='flex flex-col justify-center items-left'>
                        <p className='-ml-12 font-semibold text-xl px-2'>{userDetails.username}</p>
                    </div>
                    {/* <img src={menuIcon} alt="menu" onClick={toggleDropdown}/> */}
                    <button className='bg-green-600 rounded-lg shadow-lg px-1 py-2 hover:bg-green-400' onClick={handleLogout}>Logout</button>
                </div>
                        {/* <p className='text-center mb-2 -ml-4'>{userDetails.email}</p> */}
            </div>
            ) : (
                <p className='text-white text-center'>Loading user details</p>
            )}
        </div>

        {/* Right side */}
        <div className='left flex flex-col justify-between items-center text-white w-3/4 h-screen p-4'>
                <h1 className='text-2xl text-center font-semibold mb-4'>Social media sentiment text analyzer</h1>
            {result ? (
                <div>
                <div className='chat flex justify-center items-center gap-4 p-4 mb-4'>
                    {/* <img src="" alt="profile img" className='w-16 h-16 bg-white' /> */}
                     <div className='w-10 h-10 bg-green-600 flex justify-center items-center rounded-full'>
                        <p className='text-white font-bold'>{userDetails.username.charAt(0).toUpperCase()}</p>
                    </div>
                    <p className='text-md w-3/4'>{result.text_input}</p>
                </div>
                <div className='output'>
                    <div className='flex justify-between'>
                        <h1 className='text-2xl font-semibold'>Output:</h1>
                        <div className='flex gap-2'>
                            <img src={copyIcon} alt="copy" className='w-6 h-6' />
                            <img src={thumbUp} alt="like" className='w-6 h-6'/>
                            <img src={thumbDown} alt="dislike" className='w-6 h-6'/>
                        </div>
                    </div>
                    {/* output results */}
                    <div className="text-center text-2xl">
                        <p>Sentiment: {result.label}</p>
                        <p>Score: {(result.score * 100).toFixed(3)} %</p>
                        {/* Display other result properties as needed */}
                    </div>
                </div>
            </div>
            ) : (
                <p className='text-center'>No results yet</p>
            
            )}

            <div className='flex flex-col items-center'>
                <div className='fle items-center mb-4'>
                    <textarea 
                        className='input px-2 py-2 pr-12 rounded' 
                        value={inputText}
                        // type="text" 
                        placeholder='Search sentiment text...'
                        onBeforeInput={handleInputChange}
                        onChange={(e) => setInputText(e.target.value)}
                    />
                    <button
                        className='-ml-10'
                        onClick={analyzeSentiment}
                    >
                        <img className='mb-1' src={searchIcon} alt="search" />
                    </button>
                </div>
                <p>Created by Slanconcept.io ©2024</p>
            </div>
        </div>

    </div>
  )
}

export default Home