import { useAuth } from '../AuthContext';
// import google from '../assets/google.svg';
import { Link, useNavigate } from 'react-router-dom';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';
// import { useState } from 'react';

const Login = () => {
    const { login } = useAuth();
    // const [userId, setUserId] = useState('');
    const navigate = useNavigate();

    const BackToHome = () => {
        navigate("/");
    }

    const formik = useFormik({
        initialValues: {
          email: '',
          password: '',
        },
        validationSchema: Yup.object({
          email: Yup.string().required('Required'),
          password: Yup.string().required('Required'),
        }),
        onSubmit: async (values, { setSubmitting, setErrors }) => {
          try {
            const response = await axios.post('http://127.0.0.1:8000/login', values, {
              withCredentials: true,
              headers: {
                'Content-Type': 'application/json',
              },
            });
            console.log('Login successful:', response.data);
            if {
                const { access_token: accessToken, user_id: userId } = response.data;
                login(accessToken, userId);
                // You can redirect or perform other actions upon successful login
                navigate("/home");
            } else {
                    navigate('/home');
                }
          } catch (error) {
            console.error('Login failed:', error.response.data);
            alert(error.response.data.detail);
            // alert('Login failed, change your password')
            // return <div>{error.response.data.detail}</div>
            setErrors(error.response.data); // Set backend errors to display on the form
          } finally {
            setSubmitting(false);
          }
        },
      });
      
  return (
    <div className='details h-screen'>
        <div className="flex pl-7 pr-7 mb-10">
            <h1 className="text-green-600 text-2xl mt-4 mb-2 font-bold" onClick={BackToHome}>Sentiment Analyzer</h1>
        </div>
        <div className='flex flex-col justify-center items-center'>
            <h2 className='text-4xl text-white font-semibold mb-5'>Welcome Back</h2>
            <div className='flex flex-row h-full rounded-lg bg-gray-50 p-4'>
                {/* <img src={loginBg} alt="loginBg" className='image'/> */}
                <div className='flex flex-col justify-center items-center m-4'>
                    <form onSubmit={formik.handleSubmit} className='flex flex-col justify-center my-8'>
                        <input
                            type="email"
                            className='border-2 w-96 border-gray-400 rounded-md p-2 m-2'
                            placeholder='Email'
                            name="email"
                            value={formik.values.email}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                        />
                        {formik.touched.email && formik.errors.email && (
                        <div className='text-red-500 px-3 text-lg'>{formik.errors.email}</div>
                        )}

                        <input
                            type="password"
                            className='border-2 w-96 border-gray-400 rounded-md p-2 m-2'
                            placeholder='Password'
                            name="password"
                            value={formik.values.password}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                        />
                        {formik.touched.password && formik.errors.password && (
                        <div className='text-red-500 px-3 text-lg'>{formik.errors.password}</div>
                        )}
                        <button
                            type='submit'
                            className='bg-green-500 hover:bg-green-400 text-white border-2 w-96 border-gray-400 rounded-md p-2 m-2'
                        >
                            Log in
                        </button>
                        <p className='text-md text-center font-normal'>Don't have an account? <Link to='/register'><span className='font-semibold text-green-500 hover:underline'>Sign up</span></Link></p>
                    </form>
                    {/* <p className='text-center font-medium m-4'>Or</p> */}
                    
                    {/* <span className='flex justify-center items-center border-2'>
                        <img src={google} alt="google" className='google' />
                        <p className='m-4 text-lg font-medium'>Google Account</p>
                    </span> */}
                </div>
            </div>
        </div>
    </div>
  )
}

export default Login;
