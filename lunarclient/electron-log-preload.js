
      try {
        (function V({contextBridge:J,ipcRenderer:K}){if(!K)return;K.on("__ELECTRON_LOG_IPC__",(te,ne)=>{window.postMessage({cmd:"message",...ne})}),K.invoke("__ELECTRON_LOG__",{cmd:"getOptions"}).catch(te=>console.error(new Error(`electron-log isn't initialized in the main process. Please call log.initialize() before. ${te.message}`)));const ee={sendToMain(te){try{K.send("__ELECTRON_LOG__",te)}catch(ne){console.error("electronLog.sendToMain ",ne,"data:",te),K.send("__ELECTRON_LOG__",{cmd:"errorHandler",error:{message:ne==null?void 0:ne.message,stack:ne==null?void 0:ne.stack},errorName:"sendToMain"})}},log(...te){ee.sendToMain({data:te,level:"info"})}};for(const te of["error","warn","info","verbose","debug","silly"])ee[te]=(...ne)=>ee.sendToMain({data:ne,level:te});if(J&&process.contextIsolated)try{J.exposeInMainWorld("__electronLog",ee)}catch{}typeof window=="object"?window.__electronLog=ee:__electronLog=ee})(require('electron'));
      } catch(e) {
        console.error(e);
      }
    