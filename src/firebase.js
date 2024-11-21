// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCxD8yIxaC-iedIB7y0K5haa6UXFofj3po",
  authDomain: "engg1320-e9961.firebaseapp.com",
  projectId: "engg1320-e9961",
  storageBucket: "engg1320-e9961.firebasestorage.app",
  messagingSenderId: "893939619541",
  appId: "1:893939619541:web:7622f3cfcfca1cf652b45c",
  measurementId: "G-864R60B7XL"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
export const auth = getAuth(app);
