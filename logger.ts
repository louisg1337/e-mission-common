export const logDebug = (message: string) =>
  window["Logger"].log(window["Logger"].LEVEL_DEBUG, message);

export const logInfo = (message: string) =>
  window["Logger"].log(window["Logger"].LEVEL_INFO, message);

export const logWarn = (message: string) =>
  window["Logger"].log(window["Logger"].LEVEL_WARN, message);

export const logError = (message: string) =>
  window["Logger"].log(window["Logger"].LEVEL_ERROR, message);
