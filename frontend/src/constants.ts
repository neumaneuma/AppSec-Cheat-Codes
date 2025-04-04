interface Config {
  API_BASE_URL: string
}

function loadConfig(): Config {
  // By default, the dev server (dev command) runs in development mode and the build command runs in
  // production mode. This means when running vite build, it will load the env variables from .env.production
  // if there is one.
  // https://vite.dev/guide/env-and-mode#modes
  const isProdDeploy = import.meta.env.VITE_PROD_DEPLOY === 'true'

  if (isProdDeploy) {
    return { API_BASE_URL: 'https://api-ctf.neumaneuma.com' }
  }

  // Default to localhost if not deploying to prod
  return { API_BASE_URL: 'http://127.0.0.1:12301' }
}

export const config = loadConfig()
export const API_BASE_URL = config.API_BASE_URL
const VULNERABLE_PATH = 'vulnerabilities'

export const SUBMISSION_URL = `${API_BASE_URL}/submission`
export const SQLI_LOGIN_BYPASS_API_VULNERABLE_URL = `${API_BASE_URL}/${VULNERABLE_PATH}/sqli1/login/`
export const SQLI_SECOND_ORDER_API_REGISTER_VULNERABLE_URL = `${API_BASE_URL}/${VULNERABLE_PATH}/sqli2/register/`
export const SQLI_SECOND_ORDER_API_CHANGE_PASSWORD_VULNERABLE_URL = `${API_BASE_URL}/${VULNERABLE_PATH}/sqli2/change_password/`
export const SSRF_WEBHOOK_API_VULNERABLE_URL = `${API_BASE_URL}/${VULNERABLE_PATH}/ssrf1/submit_webhook/`
export const SSRF_LOCAL_FILE_API_VULNERABLE_URL = `${API_BASE_URL}/${VULNERABLE_PATH}/ssrf2/submit_api_url/`
