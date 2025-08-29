import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const setTokens = (tokens: { accesstoken: string; refreshtoken: string; expires_on?: string }) => {
  localStorage.setItem('accesstoken', tokens.accesstoken);
  localStorage.setItem('refreshtoken', tokens.refreshtoken);
  if (tokens.expires_on) localStorage.setItem('expires_on', tokens.expires_on);
};

export const getTokens = () => {
  const accesstoken = localStorage.getItem('accesstoken');
  const refreshtoken = localStorage.getItem('refreshtoken');
  const expires_on = localStorage.getItem('expires_on');
  if (!accesstoken || !refreshtoken) return null;
  return { accesstoken, refreshtoken, expires_on };
};

export const clearTokens = () => {
  localStorage.removeItem('accesstoken');
  localStorage.removeItem('refreshtoken');
  localStorage.removeItem('expires_on');
};

export const isTokenExpired = (accessToken: string) => {
  try {
    const payload = JSON.parse(atob(accessToken.split('.')[1]));
    const exp = payload.exp * 1000;
    return Date.now() >= exp;
  } catch {
    return true;
  }
};
