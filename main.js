const { app, BrowserWindow, session, shell } = require('electron');
const path = require('path');
function createWindow(){
  const win = new BrowserWindow({width:1440,height:900,minWidth:960,minHeight:640,
    backgroundColor:'#0d0e11', autoHideMenuBar:true,
    webPreferences:{preload:path.join(__dirname,'preload.js'),contextIsolation:true,nodeIntegration:false, sandbox:true}});
  win.loadFile(path.join(__dirname,'board','index.html'));
  win.webContents.setWindowOpenHandler(({url})=>{ if(/^https?:/.test(url)) shell.openExternal(url); return {action:'deny'}; });
  win.webContents.on('will-navigate',(e,url)=>{ if(!url.startsWith('file://')) e.preventDefault(); });
}
app.whenReady().then(()=>{
  session.defaultSession.setPermissionRequestHandler((webContents,permission,callback)=>{
    callback(['media','camera','microphone','audioCapture','videoCapture'].includes(permission));
  });
  session.defaultSession.setPermissionCheckHandler((_wc,permission)=>['media','camera','microphone','audioCapture','videoCapture'].includes(permission));
  createWindow();
  app.on('activate',()=>{if(BrowserWindow.getAllWindows().length===0) createWindow();});
});
app.on('window-all-closed',()=>{if(process.platform!=='darwin')app.quit();});
