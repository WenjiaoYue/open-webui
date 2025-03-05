import { browser } from '$app/environment';
import { PublicClientApplication } from '@azure/msal-browser';

let msalInstance;

// if (browser) {
//   const msalConfig = {
//     auth: {
//         clientId: '4690c9f2-1ced-445c-bdae-cdbf12c6c763',
//         authority: 'https://login.microsoftonline.com/e6d1ac85-3c90-40a6-8248-ae892b591b46',
//         redirectUri: window.location.origin,
//         postLogoutRedirectUri: window.location.origin
//     },
//     cache: {
//       cacheLocation: 'sessionStorage',
//       storeAuthStateInCookie: false
//     }
//   };

//   msalInstance = new PublicClientApplication(msalConfig);
// }

if (browser) {
  const msalConfig = {
    auth: {
        clientId: '7db34832-e8e8-4af4-b582-1a73a50234cd',
        authority: 'https://login.microsoftonline.com/46c98d88-e344-4ed4-8496-4ed7712e255d',
        redirectUri: window.location.origin,
        postLogoutRedirectUri: window.location.origin
    },
    cache: {
      cacheLocation: 'sessionStorage',
      storeAuthStateInCookie: false
    }
  };

  msalInstance = new PublicClientApplication(msalConfig);
}

export { msalInstance };
