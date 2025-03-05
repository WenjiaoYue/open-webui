import { msalInstance } from './msalConfig';
import { writable } from 'svelte/store';

export const isAuthenticated = writable(false);
export const MicroSoftUser = writable(null);

export const initializeMsal = async () => {
  try {
    if (!msalInstance.getActiveAccount()) {
      await msalInstance.initialize();
    }
  } catch (error) {
    console.error('MSAL 初始化错误:', error);
  }
};

export const MicrosoftAuthLogin = async () => {
  try {
    await initializeMsal(); 
    const loginResponse = await msalInstance.loginPopup({
      scopes: ['user.read', 'openid', 'profile'],
      prompt: 'select_account', 
    });
    msalInstance.setActiveAccount(loginResponse.account);
    console.log('loginResponse', loginResponse);
    
    MicroSoftUser.set(loginResponse.account);
    isAuthenticated.set(true);

    return loginResponse
  } catch (error) {
    console.error('登录错误:', error);
  }
};


export const MicrosoftAuthLogout = async () => {
  try {
    await initializeMsal(); 
    await msalInstance.logoutRedirect({
      postLogoutRedirectUri: window.location.origin, 
    });
    isAuthenticated.set(false);
    MicroSoftUser.set(null);
  } catch (error) {
    console.error('登出错误:', error);
    location.href = '/auth';

  }
};

export const handleRedirect = async () => {
  try {
    await initializeMsal(); 
    const response = await msalInstance.handleRedirectPromise();
    if (response) {
      msalInstance.setActiveAccount(response.account);
      MicroSoftUser.set(response.account);
      isAuthenticated.set(true);
    } else {
      const account = msalInstance.getAllAccounts()[0];
      if (account) {
        msalInstance.setActiveAccount(account);
        MicroSoftUser.set(account);
        isAuthenticated.set(true);
      }
    }
  } catch (error) {
    console.error('处理重定向错误:', error);
  }
};