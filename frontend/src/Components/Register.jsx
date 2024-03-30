// import logo from '../assets/logo.svg';
// import registerBg from '../assets/registerBg.png';
// import google from '../assets/google.svg';
import { Link, useNavigate } from 'react-router-dom';
import { useFormik } from 'formik';
import * as Yup from 'yup';
// import axios from 'axios';

const Register = () => {
    const navigate = useNavigate();

    const BackToHome = () => {
        navigate("/");
    }

    const formik = useFormik({
        initialValues: {
          username: '',
          fullname: '',
          email: '',
          password: '',
        },
        validationSchema: Yup.object({
          username: Yup.string(),
          fullname: Yup.string(),
          email: Yup.string().email('Invalid email address').required('Required'),
          password: Yup.string().min(8, 'Password must be at least 8 characters').required('Required'),
        }),
        onSubmit: async (values) => {
            try {
                const response = await fetch('http://127.0.0.1:8000/signup', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(values),
                    });

                if (!response.ok) {
                    const errorData = await response.json();
                    console.error('Error:', errorData);
                } else if {
                    const responseData = await response.json();
                    console.log('Success:', responseData);
                    navigate('/home');
                }
                else {
                    navigate('/home');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        },
      });

    return (
        <div className='details h-screen'>
           <div className="flex pl-7 pr-7 mb-10">
                <h1 className="text-green-600 text-2xl mt-4 mb-2 font-bold" onClick={BackToHome}>Sentiment Analyzer</h1>
            </div>
            <div className='flex flex-col justify-center items-center'>
                <h2 className='text-4xl text-white font-semibold mb-5'>Create An account</h2>
                <div className='flex flex-row border-2 h-full bg-gray-50 rounded-lg p-4'>
                    {/* <img src={registerBg} alt="loginBg" className='image'/> */}
                    <div className='flex flex-col justify-center items-center m-4'>
                        <form onSubmit={formik.handleSubmit} className='flex flex-col justify-center m-4'>
                        <input
                              type="text"
                              placeholder='Username'
                              name="username"
                              value={formik.values.username}
                              onChange={formik.handleChange}
                              onBlur={formik.handleBlur}
                              className='border-2 w-96 border-gray-400 rounded-md p-2 m-2' 
                            />
                            {formik.touched.username && formik.errors.username && (
                            <div className='text-red-500 px-3 text-lg'>{formik.errors.username}</div>
                            )}
                            <input
                              type="text"
                              placeholder='Email'
                              name="email"
                              value={formik.values.email}
                              onChange={formik.handleChange}
                              onBlur={formik.handleBlur}
                              className='border-2 w-96 border-gray-400 rounded-md p-2 m-2' 
                            />
                            {formik.touched.email && formik.errors.email && (
                            <div className='text-red-500 px-3 text-lg'>{formik.errors.email}</div>
                            )}
                            <input
                              type="password"
                              placeholder='Password'
                              name="password"
                              value={formik.values.password}
                              onChange={formik.handleChange}
                              onBlur={formik.handleBlur}
                              className='border-2 w-96 border-gray-400 rounded-md p-2 m-2'
                            />
                            {formik.touched.password && formik.errors.password && (
                            <div className='text-red-500 px-3 text-lg'>{formik.errors.password}</div>
                            )}
                            <button
                              type='submit'
                              className='bg-green-500 hover:bg-green-400 text-white border-2 w-96 border-gray-400 rounded-md p-2 m-2'
                            >
                                Sign up
                            </button>
                            <p className='text-md text-center font-normal'>Already have an account? <Link to='/login'><span className='font-semibold text-green-500 hover:underline'>Log in</span></Link></p>
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

export default Register;
