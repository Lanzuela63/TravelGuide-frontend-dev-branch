import * as Device from 'expo-device';
import { NGROK_URL, LOCAL_URL, PROD_API_BASE_URL } from '@env';

declare const __DEV__: boolean;

let DEV_API_BASE_URL: string;

if (__DEV__) {
  if (Device.isDevice) {
    DEV_API_BASE_URL = NGROK_URL;
  } else {
    DEV_API_BASE_URL = LOCAL_URL;
  }
} else {
  DEV_API_BASE_URL = PROD_API_BASE_URL;
}

export const API_BASE_URL: string = DEV_API_BASE_URL;
export const AR_BASE_URL: string = __DEV__ ? (Device.isDevice ? NGROK_URL : LOCAL_URL) + '/ar' : 'https://bicol-ar-tourism.onrender.com';