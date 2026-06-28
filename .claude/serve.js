const http=require('http'),fs=require('fs'),path=require('path');
const ROOT=path.join(__dirname,'..','output','agent-team-builder');
const PORT=process.env.PORT||8731;
const T={'.html':'text/html;charset=utf-8','.png':'image/png','.css':'text/css','.js':'text/javascript'};
http.createServer((req,res)=>{
  let p=decodeURIComponent(req.url.split('?')[0]); if(p==='/')p='/index.html';
  const f=path.join(ROOT,p);
  if(!f.startsWith(ROOT)){res.writeHead(403);return res.end();}
  fs.readFile(f,(e,d)=>{ if(e){res.writeHead(404);return res.end('404');}
    res.writeHead(200,{'Content-Type':T[path.extname(f)]||'application/octet-stream'});res.end(d);});
}).listen(PORT,()=>console.log('serving on '+PORT));
