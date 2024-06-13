/// <reference types="vite/client" />
/// <reference types="vite-plugin-svgr/client" />

declare const APP_VERSION: string;
interface ImportMetaEnv {
  VITE_API_BASE_URL: string;
}
