import React, { useEffect, useState } from "react";
import logo from "../assist/images/Logo.png";
import loginScreenImage from "../assist/images/login-screen-image.svg";
import { InputField } from "../components/common/Form";
import { BASE_URLS } from "../ApiEndPoints";
import { useDispatch } from "react-redux";
import { setOpenLoader } from "../redux/dataSlice";
import { ErrorAlert } from "../components/common/Alert";
import { toast } from "react-toastify";
import { useApi } from "../common/useApi";
import { fetchAndStoreTenantInfo } from "../localStore/TenantInfo";
import { fetchAndStorePermissionInfo } from "../localStore/TenantPermission";
import { set } from "date-fns";
// import { useNavigate } from "react-router-dom";

const Login = ({ setIsLoggedIn }) => {

  const dispatch = useDispatch();
  const [companyName, setCompanyName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showAlert, setShowAlert] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const { fetchApiRequest } = useApi();

  const addPatient = async (patientData) => {
    // console.log("in");
    dispatch(setOpenLoader(true));
    const url = `/api/auth/v2/login`;
    const body = {
      userName: email,
      password: password,
      tenant: companyName,
    };
    let showSuccessToast = true;
    let showErrorToast = true;
    let successMessage = "Login Success!";
    let errorMessage = "Something went wrong";
    try {
      const response = await fetchApiRequest({
          url:url,
          method: "POST",
          body,
          showSuccessToast: false,
          showErrorToast: false,
        });

      if (response.responseCode===200) {
        setIsLoggedIn(true);
        if(!response.tenant && !response.role)
        {
          toast.error("Tenant or Role not assigned. Please contact administrator.");

        }

        localStorage.setItem("userName", response.name);
        localStorage.setItem("role", response.role);
        localStorage.setItem("tenant", response.tenant);
        localStorage.setItem("name", response.name);
        fetchAndStoreTenantInfo(response.tenant)
        fetchAndStorePermissionInfo(response.tenant,response.role)
      } else {
        setShowAlert(true);
      }
      // if (!response.ok) {
      //   throw new Error(
      //     response?.message || "Unable to login : " + response?.statusText
      //   );
      // }

      if (response.responseCode === 401) {
        if (showErrorToast) toast.error(response?.responseMessage);
        setErrorMsg("error please enter valid data!");
      } else if (response.responseCode === 402) {
        if (showErrorToast)
          toast.error(response?.responseMessage, { toastId: "api-error" });
        setErrorMsg("Account is inactive. Please contact administrator.");
        return
      }
    } catch (error) {
      console.error("API Error:", error);
      if (showErrorToast)
        toast.error(error.message || errorMessage, { toastId: "api-error" });

      if (error.message === "Failed to fetch") localStorage.clear();
    }
    dispatch(setOpenLoader(false));

  };

  // function handleLogin(params) {
  //   if (
  //     companyName === "ayurved" &&
  //     email === "hspdm" &&
  //     password === "test@1234"
  //   ) {
  //     localStorage.setItem("token", "login");
  //     // navigate("/");
  //   } else {
  //     console.log("Envalid username or password");
  //   }
  // }

  useEffect(() => {

    // if(localStorage.getItem("Authorization")==="" || localStorage.getItem("Authorization")===null)
    //   setIsLoggedIn(false)

    const wakeUpServices = async () => {
      try {
        await fetchApiRequest({
          url: `/api/auth/v2/wake-up`,
          method: "GET",
          showSuccessToast: false,
          showErrorToast: false,
        });

        await fetchApiRequest({
          url: `/api/case/v1/wake-up`,
          method: "GET",
          showSuccessToast: false,
          showErrorToast: false,
        });

        await fetchApiRequest({
          url: `/patient/api/v1/wake-up`,
          method: "GET",
          showSuccessToast: false,
          showErrorToast: false,
        });

        await fetchApiRequest({
          url: `/form/api/v1/wake-up`,
          method: "GET",
          showSuccessToast: false,
          showErrorToast: false,
        });

        await fetchApiRequest({
          url: `/appointment/api/v1/wake-up`,
          method: "GET",
          showSuccessToast: false,
          showErrorToast: false,
        });

      } catch (error) {
        console.error("Error waking up services:", error);
      }
    };
    //wakeUpServices();
  }, []);

  return (
    <div className="bg-gray-100 flex items-center justify-center h-screen overflow-y-auto px-4">
      <div className="flex flex-col md:flex-row w-full max-w-6xl bg-white shadow-lg rounded-lg overflow-hidden">
        {/* <!-- Left Panel --> */}
        <div className="md:w-[55%] bg-green-200 flex flex-col justify-center items-center">
          <img
            // src="https://via.placeholder.com/150x150?text=Doctor+Image"
            src={loginScreenImage}
            alt="Doctor Illustration"
            className=" w-full h-full object-fill"
          />
          {/* <div className="bg-white p-4 rounded-lg shadow-md w-full max-w-sm">
            <p className="font-semibold mb-2">Provider</p>
            <div className="space-y-2">
              <div className="h-2 bg-green-500 rounded-full w-3/4"></div>
              <div className="h-2 bg-green-400 rounded-full w-1/2"></div>
              <div className="h-2 bg-green-300 rounded-full w-2/3"></div>
            </div>
            <div className="mt-4 flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">
                Subscription
              </span>
              <div className="h-8 w-8 bg-green-500 rounded-full flex items-center justify-center text-white font-bold">
                +
              </div>
            </div>
          </div> */}
        </div>

        {/* <!-- Right Panel (Login Form) --> */}
        <div className="md:w-[45%] w-full p-8 sm:p-16">
          <div className="flex flex-col justify-center h-full">
            <div className="mb-8">
              <img
                // src="https://via.placeholder.com/150x40?text=MEDSQUARE"
                src={logo}
                alt="MEDSQUARE Logo"
                className="h-10 m-auto mb-4"
              />
              <h2 className="text-2xl font-bold text-gray-800">Sign In</h2>
            </div>
            {/* <form className="space-y-4"> */}
            <div className="space-y-4">
              {/* <div>
                <label className="block text-start text-sm font-medium text-gray-700">
                  Company
                </label>
                <input
                  type="text"
                  placeholder="ayurveda"
                  className="w-full mt-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
                />
              </div> */}
              <InputField
                onChange={(e) => setCompanyName(e.target.value)}
                label="Company"
                placeholder="ayurveda"
                name="company"
                value={companyName}
                required="true"
                error={errorMsg}
              />
              <div>
                {/* <label className="block text-start text-sm font-medium text-gray-700">
                  Email
                </label>
                <input
                  type="email"
                  placeholder="example@domain.com"
                  className="w-full mt-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
                /> */}
                <InputField
                  onChange={(e) => setEmail(e.target.value)}
                  label="Email"
                  name="email"
                  placeholder="example@domain.com"
                  value={email}
                  required="true"
                  error={errorMsg}
                />
              </div>
              <div>
                {/* <label className="block text-start text-sm font-medium text-gray-700">
                  Password
                </label>
                <input
                  type="password"
                  placeholder="••••••••"
                  className="w-full mt-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
                /> */}
                <InputField
                  onChange={(e) => setPassword(e.target.value)}
                  label="Password"
                  name="password"
                  placeholder="••••••••"
                  value={password}
                  type="password"
                  required="true"
                  error={errorMsg}
                />
              </div>
              <div className="flex items-center">
                <input
                  id="remember"
                  type="checkbox"
                  className="h-4 w-4 text-green-500 focus:ring-green-400 border-gray-300 rounded"
                />
                <label
                  for="remember"
                  className="ml-2 block text-sm text-gray-700"
                >
                  Remember me on this device
                </label>
              </div>
              <button
                type="submit"
                className="w-full bg-green-500 text-white py-2 rounded-md hover:bg-green-600 transition duration-200"
                onClick={() =>
                  // handleLogin()}
                  addPatient()
                }
                disabled={
                  companyName === "" && email === "" && password === ""
                    ? true
                    : false
                }
              >
                Log In
              </button>
            </div>
            {/* </form> */}
            <div className="mt-4 text-center">
              <button className="text-sm text-green-600 hover:underline bg-transparent border-none cursor-pointer">
                Forgot Password
              </button>
            </div>
          </div>
        </div>
      </div>
      {/* <p>{showAlert ? "true" : "false"} a</p> */}
      {showAlert && (
        <ErrorAlert id="error-1" openAlert={true} alertMessage={errorMsg} />
      )}
    </div>
  );
};

export default Login;
